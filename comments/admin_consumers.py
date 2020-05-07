# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import  ChannelMessage
import uuid

class CommentsConsumerAdmin(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'comments_%s' % self.room_name
        self.user_id = str(uuid.uuid4())

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.push_old_messages()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_message(self, message):
        await  self.send(text_data=json.dumps(message))

    def get_old_messages(self):
        old_messages = ChannelMessage.objects.filter(channel_name=self.room_group_name).all()
        messages = []
        for message in old_messages:
            messages.append({'command':'add', 'id':message.id, 'message':message.message, 'username':message.user_name})
        return messages

    async def push_old_messages(self):
        old_messages = await database_sync_to_async(self.get_old_messages)()
        for message in old_messages:
            await  self.send_message(message)

    @database_sync_to_async
    def add_message(self, username, message):
        channel_message = ChannelMessage()
        channel_message.user_id = self.user_id
        channel_message.channel_name = self.room_group_name
        channel_message.user_name = username
        channel_message.message = message
        channel_message.votes = 0
        channel_message.save()
        return channel_message.id
    @database_sync_to_async
    def delete_message(self, id):

        channel_message = ChannelMessage.objects.get(id=id)
        print(channel_message.user_id, self.user_id)
        channel_message.delete()
        return 'OK'

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        if command == 'add':
            message = text_data_json['message']
            username = text_data_json['username']
            message_id = await self.add_message(username, message)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'command' : command,
                    'id':message_id,
                    'username': username,
                    'message': message
                }
            )
        elif command == 'delete':
            id = text_data_json['id']
            s = await self.delete_message(id)
            print(s)
            if s != "OK":
                command="delete_error"
                await self.send(text_data=json.dumps({
                    'command': command,
                }))
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'command': command,
                        'id': id,

                    }
                )

    # Receive message from room group
    async def chat_message(self, event):
        command = event['command']
        if command == 'add':
            username = event['username']
            message = event['message']
            id = event['id']
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'command' : command,
                'message': message,
                'id': id,
                'username': username
            }))
        elif command == 'delete':
            id = event['id']

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'command': command,
                'id' : id,
            }))
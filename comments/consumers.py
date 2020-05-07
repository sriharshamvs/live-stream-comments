# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import  ChannelMessage
from django.utils import  timesince
import uuid

class CommentsConsumer(AsyncWebsocketConsumer):
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
        await self.send(text_data=json.dumps({
            'command': 'register',
            'id': self.user_id,
        }))

#        await self.push_old_messages()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_message(self, message):
        await  self.send(text_data=json.dumps(message))

    def get_old_messages(self, start, stop):
        old_messages = ChannelMessage.objects.filter(channel_name=self.room_group_name).order_by('-created_at')[start:stop]
        messages = []
        for message in old_messages:
            messages.append({'command':'get_message',
                             'id':message.id,
                             'user_id': message.user_id,
                             'message':message.message,
                             'username':message.user_name,
                             'created_at': timesince.timesince(message.created_at)})
        return messages
    
    def get_pinned_messages(self):
        old_messages = ChannelMessage.objects.filter(channel_name=self.room_group_name, pinned=True).order_by('-created_at')
        messages = []
        for message in old_messages:
            messages.append({'command':'get_pinned_message',
                             'id':message.id,
                             'user_id': message.user_id,
                             'message':message.message,
                             'username':message.user_name,
                             'created_at': timesince.timesince(message.created_at)})
        return messages


    async def push_old_messages(self, start, stop):
        old_messages = await database_sync_to_async(self.get_old_messages)(start, stop)
        for message in old_messages:
            await  self.send_message(message)
    
    async def send_pinned_messages(self):
        old_messages = await database_sync_to_async(self.get_pinned_messages)()
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
        channel_message.pinned = False
        channel_message.save()
        return channel_message.id

    @database_sync_to_async
    def delete_message(self, id):

        channel_message = ChannelMessage.objects.get(id=id)
        print(channel_message.user_id, self.user_id)
        if channel_message.user_id == self.user_id:
            channel_message.delete()
            return "OK"
        else:
            return "NOK"

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
                    'user_id':self.user_id,
                    'username': username,
                    'message': message
                }
            )
        elif command == 'get_messages':
            startIndex = int(text_data_json['start']);
            stopIndex  = int(text_data_json['stop']);
            await self.push_old_messages(startIndex, stopIndex)

        elif command == 'get_pinned_messages':
            
            await self.send_pinned_messages()

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
                'user_id':event['user_id'],
                'username': username
            }))
        elif command == 'get_pinned_messages':
            await self.send_message({'command':'clear_pins'})
            await self.send_pinned_messages()
        elif command == 'delete':
            id = event['id']

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'command': command,
                'id' : id,
            }))

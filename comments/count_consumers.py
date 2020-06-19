# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import  ChannelMessage
from django.utils import  timesince
import uuid

class CountConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'count_%s' % self.room_name
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


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']


        if command == 'update':
            count = int(text_data_json['count'])
            self.user_id = text_data_json['id']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'command' : command,
                    'id':self.user_id,
                    'count': count
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        command = event['command']
        if command == 'update':
            id = event['id']
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'command' : 'upd',
                'id': id,
                'count':event['count']
            }))

# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import  ChannelMessage, Channel, IPAddress, ChannelSession
from django.utils import  timesince
import uuid
import datetime

class CommentsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        
        exists = await self.channel_exists()
        print(self.room_group_name, exists)
        if exists:
        # Join room group
            self.channel = exists
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
	
            await self.accept()
            self.client_address = self.scope['client'][0]
            self.user_id = str(uuid.uuid4()) # Changing user id from IP to uuid.
            #self.user_id = self.scope['client'][0]
            self.ip_obj = await self.register_ip(self.client_address)
            self.channel_session = await self.register_session()
            await self.send_join_message()
            await self.send(text_data=json.dumps({
                'command': 'register',
                'id': self.user_id,
            }))
        
#        print(self.scope['client'])
#        await self.push_old_messages()



    async def disconnect(self, close_code):
        # Leave room group
        await self.send_join_message(state="leave")
        await self.deregister_session()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_message(self, message):
        await  self.send(text_data=json.dumps(message))

    def get_old_messages(self, start, stop):
        
        old_messages = ChannelMessage.objects.filter(channel=self.channel, approved=True).order_by('-created_at')[start:stop]
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
        old_messages = ChannelMessage.objects.filter(channel=self.channel, pinned=True, approved=True).order_by('-created_at')
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
    def channel_exists(self):
        channel = Channel.objects.filter(channel_name = self.room_group_name)
        if channel:
             return channel.all()[0]
        return False

    @database_sync_to_async
    def register_ip(self, ip_address):
        ip = IPAddress.objects.filter(ip_address=ip_address)
        if ip:
             return ip.all()[0]
        else:
            ip = IPAddress()
            ip.ip_address = ip_address
            ip.blocked = False
            ip.save()
            return ip
            
    @database_sync_to_async
    def register_session(self):
        cs = ChannelSession()
        
        channel = Channel.objects.filter(channel_name = self.room_group_name)
        if channel:
            cs.channel = channel[0]
            cs.user_id = self.user_id
            cs.user_name = ''
            cs.online = True
            cs.save()

            return cs
        return False
    
    @database_sync_to_async
    def deregister_session(self):
        channel = Channel.objects.filter(channel_name = self.room_group_name)
        if channel:
            self.channel_session.ended_at = datetime.datetime.now()
            self.channel_session.online = False
            self.channel_session.save()

    async def send_join_message(self, state="join"):
        await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'command' : state,
                            'user_id':self.user_id,
                            'username': self.channel_session.user_name,                           
                        }
                    )


    @database_sync_to_async
    def add_message(self, username, message):
       
        channel = Channel.objects.filter(channel_name = self.room_group_name)
        if channel:
             self.channel = channel.all()[0]
             channel_message = ChannelMessage()
             channel_message.user_id = self.user_id
             channel_message.channel = self.channel
             channel_message.user_name = username
             channel_message.message = message
             channel_message.votes = 0
             channel_message.pinned = False
        
             channel_message.approved = not self.channel.moderate
             ip_address = IPAddress.objects.filter(ip_address=self.client_address)
             if ip_address:
                ip_address = ip_address.all()[0]
             else:
                ip_address = IPAddress(ip_address = self.client_address, blocked=False)
                ip_address.save()
             if ip_address.blocked:
                channel_message.approved = False 
             channel_message.ip_address = ip_address
             channel_message.save()
             
             if self.channel_session:
                 self.channel_session.user_name = username
                 self.channel_session.save()

             return channel_message.id, channel_message.approved, channel_message.user_id
        else:
            print(f"Cannot find channel {channel}")

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
            if 'http' not in message:
                username = text_data_json['username']
                result = await self.add_message(username, message)
                if result:
                    message_id, approved, user_id = result
                    # Send message to room group
#                   cmd = 'moderate_message' if not approved else 'add'
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'command' : 'add',
                            'id':message_id,
                            'user_id':user_id,
                            'username': username,
                            'approved':approved,
                            'message': message
                        }
                    )
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'command' : 'change_name',
                            'user_id':self.user_id,
                            'username': self.channel_session.user_name,                           
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
        if command == 'moderate_message':
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
                'username': username,
                'approved':event['approved']
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
#        elif command in ["join", "leave", "change_name"]:
#            await self.send(text_data=json.dumps({
#                'command': command,
#                'user_id': event['user_id'],
#                'username': event['username']
#            }))

# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import  *
from django.utils import  timesince
import uuid

class CommentsConsumerAdmin(AsyncWebsocketConsumer):
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
            self.user_id = self.scope['client'][0]
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
        old_messages = ChannelMessage.objects.filter(channel=self.channel).order_by('-created_at')[start:stop]
        messages = []
        for message in old_messages:
            messages.append({'command':'get_message',
                             'id':message.id,
                             'user_id': message.user_id,
                             'message':message.message,
                             'username':message.user_name,
                             'approved':message.approved,
                             'blocked':message.ip_address.blocked,
                             'created_at': timesince.timesince(message.created_at)})
        return messages

    def get_old_users(self):
        old_users  = ChannelSession.objects.filter(channel=self.channel, online=True).order_by('user_name')
        print(old_users)
        users  = []
        for user in old_users :
            users.append({'command':'join',
                          'user_id': user.user_id,
                          'username':user.user_name,
                        })
        return users 


    def get_pinned_messages(self):
        old_messages = ChannelMessage.objects.filter(channel=self.channel, pinned=True).order_by('-created_at')
        messages = []
        for message in old_messages:
            messages.append({'command':'get_pinned_message',
                             'id':message.id,
                             'user_id': message.user_id,
                             'message':message.message,
                             'username':message.user_name,
                             'approved' : message.approved,
                             'blocked':message.ip_address.blocked,
                             'created_at': timesince.timesince(message.created_at)})
        return messages
    
    async def push_old_users(self):
        old_users = await database_sync_to_async(self.get_old_users)()        
        for user in old_users:
            await  self.send_message(user)


    async def push_old_messages(self, start, stop):
        old_messages = await database_sync_to_async(self.get_old_messages)(start, stop)     
        for message in old_messages:
            await  self.send_message(message)


    async def send_pinned_messages(self):
        old_messages = await database_sync_to_async(self.get_pinned_messages)()
        for message in old_messages:
            await  self.send_message(message)


    @database_sync_to_async
    def toggle_pin_message(self, message_id, pin = True):
		
        channel_message = ChannelMessage.objects.get(id=message_id)

        channel_message.pinned = pin
        channel_message.save()

    @database_sync_to_async
    def approve_message(self, message_id, approve = True):
		
        channel_message = ChannelMessage.objects.get(id=message_id)

        channel_message.approved = approve
        channel_message.save()
        return channel_message.ip_address.id, channel_message.user_name, channel_message.message

    @database_sync_to_async
    def channel_exists(self):
        channel = Channel.objects.filter(channel_name = self.room_group_name)
        if channel:
             return channel.all()[0]
        return False

    @database_sync_to_async
    def get_message_ip(self, id):
        channel = ChannelMessage.objects.get(id = id)
        if channel:
           return channel.ip_address.ip_address, channel.ip_address.blocked
         
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
        
             channel_message.approved = True
             ip_address = IPAddress.objects.filter(ip_address=self.user_id)
             if ip_address:
                ip_address = ip_address.all()[0]
             else:
                ip_address = IPAddress(ip_address = self.user_id, blocked=False)
                ip_address.save()
             channel_message.ip_address = ip_address
             channel_message.save()
             return channel_message.id, channel_message.approved
        else:
            print(f"Cannot find channel {channel}")
    @database_sync_to_async
    def delete_message(self, id):

        channel_message = ChannelMessage.objects.get(id=id)
        print(channel_message.user_id, self.user_id)
        channel_message.delete()
        return "OK"

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']


        if command == 'add':
            message = text_data_json['message']
            username = text_data_json['username']
            message_id, approved = await self.add_message(username, message)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'command' : command,
                    'id':message_id,
                    'user_id':self.user_id,
                    'username': username,
                    'approved':approved,
                    'message': message
                }
            )
        elif command == 'approve_message':
#            message = text_data_json['message']
#            username = text_data_json['username']
            print("Jelllo !")           
            user_id, user_name, message = await self.approve_message(text_data_json['id'], approve = True)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'command' : 'add',
                    'id':text_data_json['id'],
                    'user_id':user_id,
                    'username': user_name,
                    'approved':True,
                    'message': message
                }
            )
        elif command == 'pin':
            await self.toggle_pin_message(int(text_data_json['id']))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'command' : 'get_pinned_messages',
                    'id':text_data_json['id'],
                    
                }
            )
        elif command == 'unpin':
            await self.toggle_pin_message(int(text_data_json['id']), pin=False)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'command' : 'get_pinned_messages',
                    'id':text_data_json['id'],
                    
                }
            )

#            await self.send_pinned_messages()

        elif command == 'get_messages':
            startIndex = int(text_data_json['start']);
            stopIndex  = int(text_data_json['stop']);
            await self.push_old_messages(startIndex, stopIndex)

        elif command == 'get_users':
            
            await self.push_old_users()

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
            user_id, blocked = await self.get_message_ip(id)
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'command' : command,
                'message': message,
                'id': id,
                'user_id':event['user_id'],
                'username': username,
                'approved':event['approved'],
                'blocked':blocked
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
        elif command in ["join", "leave", "change_name"]:
            
            await self.send(text_data=json.dumps({
                'command': command,
                'user_id': event['user_id'],
                'username': event['username']
            }))

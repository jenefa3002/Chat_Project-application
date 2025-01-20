import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'public_chat'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = self.scope['user'].username  # Get the username of the sender

        # Save the message to the database
        user = User.objects.get(username=username)
        Message.objects.create(user=user, content=message)

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))


    # Notify all users when a new user joins
    async def user_joined(self, event):
        await self.send(text_data=json.dumps({
            'info': f"{event['username']} joined the chat."
        }))

    # Notify all users when a user leaves
    async def user_left(self, event):
        await self.send(text_data=json.dumps({
            'info': f"{event['username']} left the chat."
        }))

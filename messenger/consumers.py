import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import UserMessages
from signup.models import UserProfile


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        user_url = text_data_json['user_url']
        user_image = text_data_json['user_image']
        await self.set_new_message(self.room_name, user_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_image': user_image,
                'user_url': user_url,
                'user_id': user_id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_image = event['user_image']
        user_url = event['user_url']
        user_id = event['user_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_image': user_image,
            'user_url': user_url,
            'user_id': user_id
        }))

    @database_sync_to_async
    def set_new_message(self, chat_id, user_id, messages):
        return UserMessages.objects.create(chat_id_id=chat_id, from_id_id=user_id, content=messages)

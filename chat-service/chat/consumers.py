from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from common.authentication import TokenUser
from channels.db import database_sync_to_async
from .models import Message


@database_sync_to_async
def save_message(room_name, sender_id, content):
    Message.objects.create(room_name=room_name, sender_id=sender_id, content=content)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode()
        params = parse_qs(query_string)
        token = params.get('token', [None])[0]
        if token is None:
            await self.close()
            return
        try:
            validated_token = AccessToken(token)
        except TokenError:
            await self.close()
            return
        user_id = validated_token.get('user_id')
        email = validated_token.get('email')
        role = validated_token.get('role')
        self.scope['user'] = TokenUser(user_id=user_id, email=email, role=role)


        user_id_1 = self.scope['url_route']['kwargs']['user_id_1']
        user_id_2 = self.scope['url_route']['kwargs']['user_id_2']
        ids = sorted([int(user_id_1), int(user_id_2)])
        current_user_id = int(self.scope['user'].id)
        if current_user_id != ids[0] and current_user_id != ids[1]:
            await self.close()
            return

        self.room_name = f'chat_{ids[0]}_{ids[1]}'
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()


    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=message)

    async def receive(self, text_data=None):
        await save_message(self.room_name, int(self.scope['user'].id), text_data)
        await self.channel_layer.group_send(self.room_name, {
            'type': 'chat_message',
            'message': text_data
        })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)


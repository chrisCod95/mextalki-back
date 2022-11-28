import json
from typing import Union

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from src.mextalki.models import Chat, ChatMessage
from src.mextalki.utils import get_user_by_uid
from src.mextalki.utils.chat import show_unread_messages, reset_unread_messages
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'test'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        chat_uuid = text_data_json['userChatUuid']
        user_id = text_data_json['user_id']

        await self.save_message(chat_uuid, message, user_id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chat_uuid': chat_uuid,
                'user_id': user_id,
            },
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chat_uuid = event['chat_uuid']
        user_id = event['user_id']

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'username': username,
            'chat_uuid': chat_uuid,
            'user_id': user_id,
        }))

    @sync_to_async
    def save_message(self, chat_uuid: str, message: ChatMessage, user_id: str) -> ChatMessage:
        try:
            chat = Chat.objects.get(chat_uuid=chat_uuid)
        except Chat.DoesNotExist as error:
            raise error
        user = get_user_by_uid(user_id)
        new_message = ChatMessage(
            chat=chat,
            content=message,
            user=user,
        )
        if reset_unread_messages(chat, user):
            chat.unread_messages = 0
            chat.save()
        new_message.save()
        chat.unread_messages += 1
        chat.save()
        return new_message

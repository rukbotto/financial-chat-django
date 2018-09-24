import datetime
import json
import re

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

from chat.models import Message, Room
from chat import tasks


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_pk = self.scope['url_route']['kwargs']['room_pk']
        self.group_name = 'chat_group_{}'.format(self.room_pk)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        content = text_data_json.get('content')
        room_pk = text_data_json.get('room_id')
        user_pk = text_data_json.get('user_id')

        match = re.match(r'/stock=([A-Z]*)', content)

        if match:
            tasks.query_quote.delay(match.group(1), room_pk, user_pk)
        else:
            room = Room.objects.get(pk=room_pk)
            user = User.objects.get(pk=user_pk)

            message = Message()
            message.content = content
            message.room = room
            message.user = user
            message.save()

            datetime = message.datetime.isoformat()
            user_name = user.username

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'send_message',
                    'datetime': datetime,
                    'content': content,
                    'room_pk': room_pk,
                    'user_pk': user_pk,
                    'user_name': user_name
                }
            )

    def send_message(self, event):
        self.send(
            text_data=json.dumps(
                {
                    'datetime': event.get('datetime'),
                    'content': event.get('content'),
                    'room_id': event.get('room_pk'),
                    'user_id': event.get('user_pk'),
                    'user_name': event.get('user_name'),
                }
            )
        )

import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

from chat.models import Message, Room


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

        room = Room.objects.get(pk=text_data_json.get('room_id'))
        user = User.objects.get(pk=text_data_json.get('user_id'))

        message = Message()
        message.datetime = parse_datetime(text_data_json.get('datetime'))
        message.content = text_data_json.get('content')
        message.room = room
        message.user = user
        message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'send_message',
                'pk': message.pk,
                'datetime': message.datetime.isoformat(),
                'content': message.content,
                'room_pk': message.room.pk,
                'user_pk': message.user.pk,
                'user_name': message.user.username,
            }
        )

    def send_message(self, event):
        self.send(
            text_data=json.dumps(
                {
                    'id': event.get('pk'),
                    'datetime': event.get('datetime'),
                    'content': event.get('content'),
                    'room_id': event.get('room_pk'),
                    'user_id': event.get('user_pk'),
                    'user_name': event.get('user_name'),
                }
            )
        )

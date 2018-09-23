from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


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
        content = text_data_json['content']

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'send_content',
                'content': content
            }
        )

    def send_content(self, event):
        content = event['content']
        self.send(
            text_data=json.dumps({ 'content': content })
        )

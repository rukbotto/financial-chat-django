from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from chat import consumers

websocket_urlpatterns = [
    url(r'^ws/room/(?P<room_pk>[^/]+)/$', consumers.ChatConsumer),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})

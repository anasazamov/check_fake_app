from django.urls import re_path
from check_app.consumer import AndroidConsumer

websocket_urlpatterns = [
    re_path(r"ws/android/$", AndroidConsumer.as_asgi()),
]

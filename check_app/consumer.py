from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
# from .ws_registry import android_clients, token_queue  # tashqaridan import qilish muhim

android_clients, token_queue = {}, {}

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)

class AndroidConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.channel_id = self.channel_name  # Har bir clientga unik kanal nomi
        android_clients[self.channel_id] = self

        await self.send(json.dumps({
            'type': 'connected',
            'channel_id': self.channel_id
        }))
        logging.info(f"Android client connected: {self.channel_id}")

    async def disconnect(self, close_code):
        android_clients.pop(self.channel_id, None)
        token_queue.pop(self.channel_id, None)
        logging.info(f"Android client disconnected: {self.channel_id}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            logging.error("JSON parsing error")
            return

        if data.get('type') == 'integrity_token':
            token = data.get('token')
            token_queue[self.channel_id] = token
            logging.info(f"Token received from {self.channel_id}: {token}")

    async def send_token(self, event):
        await self.send(text_data=json.dumps({
            'type': 'token_request'
        }))
        logging.info(f"Token request sent to {self.channel_id}")

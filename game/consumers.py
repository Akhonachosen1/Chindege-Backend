import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("game_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("game_updates", self.channel_name)

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({
            'message': 'pong'
        }))

    async def send_multiplier(self, event):
        await self.send(text_data=json.dumps({
            'multiplier': event['multiplier']
        }))

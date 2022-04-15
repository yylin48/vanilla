import imp
import json
from os import sync
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from .models import Coin


class CoinConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        await self.channel_layer.group_add('coins', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('coins', self.channel_name)

    async def send_new_data(self, event):
        coin_data = event['data']
        await self.send(json.dumps(coin_data))

    async def receive(self, text_data):
        coin_symbols = json.loads(text_data)
        print(coin_symbols['message'])
        coin_1 = coin_symbols['message'][0]
        coin_2 = coin_symbols['message'][1]
        coins = await sync_to_async(Coin.objects.all())

        print(coins)

        # 发送消息到频道组，频道组调用chat_message方法

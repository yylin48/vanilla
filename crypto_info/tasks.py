import requests
from asgiref.sync import async_to_sync
from django.forms.models import model_to_dict
from celery import shared_task
from .models import Coin
from channels.layers import get_channel_layer


from bs4 import BeautifulSoup
from .models import CryptoNews
from telegram.bot import Bot
from datetime import datetime


channel_layer = get_channel_layer()

coin_list = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'LTCUSDT', 'ADAUSDT', 'LUNAUSDT',
    'XRPUSDT', 'SOLUSDT', 'AVAXUSDT', 'DOGEUSDT', 'MATICUSDT'
]


@shared_task
def get_coins_data_binance():
    coin_data = []
    for coin in coin_list:
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={coin}'
        coin_data_dict = requests.get(url).json()

        # edit the price as float
        coin_data_dict['price'] = round(float(coin_data_dict['price']), 3)

        #store into db
        obj, created = Coin.objects.get_or_create(
            symbol=coin_data_dict['symbol'])
        obj.symbol = coin_data_dict['symbol']

        if obj.price > coin_data_dict['price']:
            state = 'fall'
        elif obj.price == coin_data_dict['price']:
            state = 'same'
        elif obj.price < coin_data_dict['price']:
            state = 'raise'
        obj.price = coin_data_dict['price']

        obj.save()

        new_coin_data = model_to_dict(obj)
        new_coin_data.update({'state': state})

        coin_data.append(new_coin_data)

    async_to_sync(channel_layer.group_send)('coins', {
        'type': 'send_new_data',
        'data': coin_data
    })



        
@shared_task
def get_binance_news():
    site = 'Binance'
    news_response = requests.get('https://www.binance.com/zh-CN/news/top?')
    soup = BeautifulSoup(news_response.content, 'lxml')
    all_news = soup.find(class_="css-18t8by3").find_all(class_="css-1i9bvdl")
   ## all_news = soup.find('div', id='news_list_body').find_all('dt')
    for news in all_news:
        # titles
        title = news.find(class_='css-yvdj0q').text
        
        # newsurl        
        news_source = news.find('a').get('href')        
        news_url = f"https://www.binance.com{news_source}"

        # imgurl
        img_url = news.find('img').get('src')
        
        #media info
        media_info = news.find(class_='css-1jackso').text

        # post_time
        post_response = requests.get(news_url)
        post_soup = BeautifulSoup(post_response.content, 'lxml')
        post_time = post_soup.find(class_='css-1hmgk20').text
        dateFormatter = "%Y-%m-%d %H:%M"
        post_time = datetime.strptime(post_time, dateFormatter)


        if not CryptoNews.objects.filter(news_url=news_url):
            CryptoNews.objects.create(news_url=news_url,
                                   title=title,
                                   img_url=img_url,
                                   media_info=media_info,
                                   post_time=post_time,
                                   site = site)
            #news_bot = Bot(TELEGRAM_BOT_API_KEY)
            # -647400651 is the chat_id of telegram group
            #news_bot.send_message('-648400651', f'{title}\n{news_url}')

##https://www.abmedia.io/category/market



"""  coingecko's price change slowly
coin_list = [
    'bitcoin', 'ethereum', 'binancecoin', 'litecoin', 'cardano', 'terra-luna',
    'ripple', 'solana', 'avalanche-2', 'dogecoin', 'matic-network'
]
def get_coins_data_coingecko(self):
    coin_url_arg=''
    for coin in coin_list:
        coin_url_arg += coin + ','
    url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin_url_arg}&order=market_cap_desc'
    coin_data_dict = requests.get(url).json()
    
    coin_data = {}
    for coin in coin_data_dict:
        
        obj, created = Coin.objects.get_or_create(symbol=coin['symbol'])
        
        obj.name = coin['name']
        obj.symbol = coin['symbol']
        obj.price = coin['current_price']
        
        coin_data_dict['price'] = round(float(coin_data_dict['price']), 2)

        coin_data.update({coin_data_dict['symbol']: coin_data_dict['price']})

    self.send(json.dumps({'LIST': coin_list, 'DICT': coin_data}))

"""

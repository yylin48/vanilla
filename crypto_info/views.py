import imp
from django.shortcuts import render
from .models import Coin, CryptoNews
# Create your views here.


def text(request):
    return render(request, 'crypto_info/text.html', {})

def coin(request):
    coin = Coin.objects.all().order_by('id')
    return render(request, 'crypto_info/coin.html', {'coin' : coin})

def news(request):
    news = CryptoNews.objects.all()
    return render(request, 'crypto_info/news.html', {'news' : news})


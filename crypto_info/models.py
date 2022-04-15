from django.db import models
from sqlalchemy import null

# Create your models here.
class CryptoNews(models.Model):
    news_url = models.URLField(max_length=200, unique=True)
    title = models.CharField(max_length=40)
    img_url = models.URLField(max_length=200)
    media_info = models.CharField(max_length=40)
    post_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    site = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class Coin(models.Model):
    #name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20)
    price = models.FloatField(default=0, blank=True)
    #rank = models.IntegerField(default=0, blank=True)
    #img_url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.symbol

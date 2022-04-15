from django.urls import path
from . import views


urlpatterns = [
    path('coin', views.coin, name='coin'),
    path('text', views.text, name='text'),
    path('news', views.news, name='news'),
]
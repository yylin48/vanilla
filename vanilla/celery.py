import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vanilla.settings')

app = Celery('vanilla')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'get_coins_data_10s' : {
        'task' : 'crypto_info.tasks.get_coins_data_binance',
        'schedule' : 10
    },
    'get_binance_news_10s' : {
        'task' : 'crypto_info.tasks.get_binance_news',
        'schedule' : 10
    }
}

app.autodiscover_tasks()
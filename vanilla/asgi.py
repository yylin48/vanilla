"""
ASGI config for vanilla project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

import crypto_info.routing

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vanilla.settings.base')

application = ProtocolTypeRouter({
    # http
    "http":
    get_asgi_application(),

    # websocket
    "websocket":
    AuthMiddlewareStack(URLRouter(crypto_info.routing.websocket_urlpattern))
})


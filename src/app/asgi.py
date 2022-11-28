import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.app.settings.production')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from src.mextalki.routing import websocket_urlpatterns

asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})

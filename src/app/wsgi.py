import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.app.settings.production')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.wsgi import get_wsgi_application

from src.mextalki.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': get_wsgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter((
                websocket_urlpatterns
            ))
        )
    )
})

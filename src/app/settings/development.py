from pathlib import Path

from paypalcheckoutsdk.core import SandboxEnvironment

from src.app.settings.base import *

ALLOWED_HOSTS = ('*',)

BASE_DIR = Path(__file__).resolve().parents[3]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PAYPAL_ENVIRONMENT = SandboxEnvironment(
    client_id=PAYPAL_CLIENT_ID,
    client_secret=PAYPAL_CLIENT_SECRET,
)
INSTALLED_APPS += ('django_extensions',)

CORS_ALLOW_ALL_ORIGINS = True

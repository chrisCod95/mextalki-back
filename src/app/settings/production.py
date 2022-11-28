from paypalcheckoutsdk.core import LiveEnvironment

from src.app.settings.base import *

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

STATIC_FILES_LOCATION = 'static'

MEDIA_FILES_LOCATION = 'media'

DEFAULT_FILE_STORAGE = 'src.app.storages.media_storage'

STATICFILES_STORAGE = 'src.app.storages.static_storage'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

PAYPAL_ENVIRONMENT = LiveEnvironment(
    client_id=PAYPAL_CLIENT_ID,
    client_secret=PAYPAL_CLIENT_SECRET,
)

TINYMCE_JS_URL = 'https://cdnjs.cloudflare.com/ajax/libs/tinymce/5.5.0/tinymce.min.js'

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

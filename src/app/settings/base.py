import os
from distutils.util import strtobool

from django.contrib.messages import constants as messages

from src.__version__ import __version__

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = bool(strtobool(os.getenv('DJANGO_DEBUG', 'False')))

ALLOWED_HOSTS = ()

INSTALLED_APPS = (
    'src.mextalki',
    'src.subscription',
    'src.users',
    'src.paypal',
    'src.api',
    'src.allauth_override',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'colorfield',
    'tinymce',
    'sort_order_field',
    'storages',
    'mathfilters',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'timezone_field',
    'nested_admin',
    'taggit',
    'fullurl',
    'django_celery_results',
    'django_celery_beat',
    'channels',
)

ASGI_APPLICATION = 'src.app.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

MIDDLEWARE = (
    'src.app.middleware.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
)

ROOT_URLCONF = 'src.app.urls'

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'src.mextalki.context_processors.seo',
                'src.mextalki.context_processors.recaptcha',
                'src.mextalki.context_processors.courses',
                'src.mextalki.context_processors.paypal',
                'src.mextalki.context_processors.google_tag_manager',
                'src.mextalki.context_processors.stripe',
                'src.mextalki.context_processors.whatsapp',
                'src.mextalki.context_processors.version',
                'src.mextalki.context_processors.announcements',
                'src.mextalki.context_processors.reminders',
            ],
            'builtins': [
                'django.templatetags.static',
            ],
        },
    },
)

WSGI_APPLICATION = 'src.app.wsgi.application'

DATABASES = {  # noqa: WPS407
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'users.User'

STATICFILES_DIRS = ()

SEO_DESCRIPTION = os.getenv('SEO_DESCRIPTION', '')

MESSAGE_TAGS = {
    messages.SUCCESS: 'alert alert-success',
    messages.WARNING: 'alert alert-warning',
    messages.INFO: 'alert alert-info',
    messages.ERROR: 'alert alert-danger',
}

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = True

SITE_ID = 1

RE_CAPTCHA_SITE_KEY = os.getenv('RE_CAPTCHA_SITE_KEY')
RE_CAPTCHA_SECRET_KEY = os.getenv('RE_CAPTCHA_SECRET_KEY')
RE_CAPTCHA_URL = os.getenv(
    'RE_CAPTCHA_URL', 'https://www.google.com/recaptcha/api/siteverify',
)

PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
PAYPAL_ENVIRONMENT = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

RESET_PASSWORD_TOKEN = os.getenv('RESET_PASSWORD_TOKEN')

GOOGLE_TAG_ID = os.getenv('GOOGLE_TAG_ID')

GOOGLE_SITE_TAG_ANALYTICS_ID = os.getenv('GOOGLE_SITE_TAG_ANALYTICS_ID')

GOOGLE_SITE_TAG_ADS_ID = os.getenv('GOOGLE_SITE_TAG_ADS_ID')

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

FREE_MIN_LESSON_TIME = int(os.getenv('FREE_MIN_LESSON_TIME', 0))
EXTRA_HOUR_LESSON_BASE_PRICE = float(os.getenv('EXTRA_HOUR_LESSON_BASE_PRICE', 24))
EXTRA_HOUR_PRACTICE_BASE_PRICE = float(os.getenv('EXTRA_HOUR_PRACTICE_BASE_PRICE', 15))
EXTRA_SEAT_CONVO_CLUB_BASE_PRICE = float(
    os.getenv('EXTRA_SEAT_CONVO_CLUB_BASE_PRICE', 5),
)
EXTRA_SEAT_CONVO_CLUB_WITH_SUBSCRIPTION_PRICE = float(
    os.getenv('EXTRA_SEAT_CONVO_CLUB_WITH_SUBSCRIPTION_PRICE', 3),
)
EXTRA_HOUR_CURRENCY = os.getenv('EXTRA_HOUR_CURRENCY', 'USD')

WHATSAPP_PHONE_NUMBER = os.getenv('WHATSAPP_PHONE_NUMBER')

CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'admin@mextalki.com')

VERSION = __version__

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            'openid',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        },
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/es/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'VERIFIED_EMAIL': True,
        'FIELDS': [
            'id',
            'name',
            'first_name',
            'last_name',
            'middle_name',
            'name_format',
            'picture',
            'short_name',
            'email',
        ],
        'VERSION': 'v12.0',
    },
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_ADAPTER = 'src.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'src.users.adapters.SocialAccountAdapter'
SOCIALACCOUNT_LOGIN_ON_GET = True

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "es_ES",  # To force a specific language instead of the Django current language.
}

CELERY_BROKER_URL = 'redis://{host}:{port}'.format(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

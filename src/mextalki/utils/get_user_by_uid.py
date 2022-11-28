import logging

from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

logger = logging.getLogger('django')

User = get_user_model()


def get_user_by_uid(user_uid_b64):
    try:
        user_uid = force_text(urlsafe_base64_decode(user_uid_b64))
        user = User.objects.get(pk=user_uid)
    except User.DoesNotExist as error:
        logger.error(error)
        user = None
    except(TypeError, ValueError, OverflowError) as error:
        logger.error(error)
        user = None
    return user

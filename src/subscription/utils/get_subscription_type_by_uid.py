from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from src.subscription.logger import logger
from src.subscription.models import SubscriptionType


def get_subscription_type_by_uid(subscription_uid_b64):
    try:
        subscription_type_uid = force_text(urlsafe_base64_decode(subscription_uid_b64))
        subscription_type = SubscriptionType.objects.get(pk=subscription_type_uid)
    except SubscriptionType.DoesNotExist as error:
        logger.error(error)
        subscription_type = None
    except(TypeError, ValueError, OverflowError) as error:
        logger.error(error)
        subscription_type = None
    return subscription_type

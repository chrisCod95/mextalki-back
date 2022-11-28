from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from src.mextalki.logger import logger
from src.mextalki.models import EventType


def get_event_type_by_uid(event_type_uid_b64):
    try:
        event_type_uid = force_text(urlsafe_base64_decode(event_type_uid_b64))
        event_type = EventType.objects.get(pk=event_type_uid)
    except EventType.DoesNotExist as error:
        logger.error(error)
        event_type = None
    except(TypeError, ValueError, OverflowError) as error:
        logger.error(error)
        event_type = None
    return event_type

import logging

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from src.mextalki.models import Teacher

logger = logging.getLogger('django')


def get_teacher_by_uid(teacher_uid_b64):
    try:
        teacher_uid = force_text(urlsafe_base64_decode(teacher_uid_b64))
        teacher = Teacher.objects.get(pk=teacher_uid)
    except Teacher.DoesNotExist as error:
        logger.error(error)
        teacher = None
    except(TypeError, ValueError, OverflowError) as error:
        logger.error(error)
        teacher = None
    return teacher

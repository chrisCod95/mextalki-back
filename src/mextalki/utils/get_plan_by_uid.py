import logging

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from src.mextalki.models import Plan

logger = logging.getLogger('django')


def get_plan_by_uid(plan_uid_b64):
    try:
        plan_uid = force_text(urlsafe_base64_decode(plan_uid_b64))
        plan = Plan.objects.get(pk=plan_uid)
    except Plan.DoesNotExist as error:
        logger.error(error)
        plan = None
    except(TypeError, ValueError, OverflowError) as error:
        logger.error(error)
        plan = None
    return plan

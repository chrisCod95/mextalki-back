import logging

from django.http import HttpResponse, HttpResponseBadRequest

from src.mextalki.paypal.api_client import get_subscription
from src.subscription.models import Subscription
from src.subscription.utils import renew_subscription

logger = logging.getLogger('django')


def _get_subscription_by_paypal_id(paypal_subscription_id: str):
    try:
        return Subscription.objects.get(provider_id=paypal_subscription_id)
    except Subscription.DoesNotExist:
        return None


def process_subscription_activated(resource):
    subscription: Subscription = _get_subscription_by_paypal_id(resource.get('id'))
    if subscription:
        subscription.status = Subscription.ACTIVE
        subscription.active = True
        subscription.next_billing_time = subscription.next_billing_time = resource[
            'billing_info'
        ]['next_billing_time']
        subscription.save()
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    return status_code


def process_subscription_cancelled(resource):
    subscription: Subscription = _get_subscription_by_paypal_id(resource.get('id'))
    if subscription:
        subscription.status = Subscription.CANCELLED
        subscription.active = False
        subscription.save()
        status_code = HttpResponse.status_code
    else:
        Subscription(
            provider=Subscription.PAYPAL,
            provider_id=resource.get('id'),
            status=resource.get('status'),
            active=False,
        ).save()
        status_code = HttpResponse.status_code
    return status_code


def process_subscription_created(resource):
    subscription: Subscription = _get_subscription_by_paypal_id(resource.get('id'))
    if subscription:
        if subscription.status is not Subscription.ACTIVE:
            subscription.status = Subscription.CREATED
        subscription.save()
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    return status_code


def process_subscription_expired(resource):
    subscription: Subscription = _get_subscription_by_paypal_id(resource.get('id'))
    if subscription:
        subscription.status = Subscription.EXPIRED
        subscription.active = False
        subscription.user.set_available_lesson_time(0)
        subscription.save()
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    return status_code


def process_subscription_payment_failed(resource):
    subscription: Subscription = _get_subscription_by_paypal_id(resource.get('id'))
    if subscription:
        subscription.status = Subscription.EXPIRED
        subscription.active = False
        subscription.user.set_available_lesson_time(0)
        subscription.save()
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    return status_code


def process_subscription_re_activated(resource):
    subscription: Subscription = _get_subscription_by_paypal_id(resource.get('id'))
    if subscription:
        subscription.status = Subscription.ACTIVE
        subscription.active = True
        subscription.next_billing_time = resource['billing_info']['next_billing_time']
        subscription.save()
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    return status_code


def process_subscription_renewed(resource):
    subscription: Subscription = _get_subscription_by_paypal_id(resource.get('id'))
    if subscription:
        subscription.status = Subscription.ACTIVE
        subscription.active = True
        subscription.next_billing_time = resource['billing_info']['next_billing_time']
        subscription.save()
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    return status_code


def process_subscription_suspended(resource):
    subscription: Subscription = _get_subscription_by_paypal_id(resource.get('id'))
    if subscription:
        subscription.status = Subscription.CANCELLED
        subscription.active = False
        subscription.user.set_available_lesson_time(0)
        subscription.save()
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    return status_code


def process_subscription_updated(resource):
    raise NotImplementedError


def payment_sale_completed(resource):
    billing_agreement_id = resource.get('billing_agreement_id')
    if billing_agreement_id:
        try:
            subscription: Subscription = _get_subscription_by_paypal_id(
                billing_agreement_id,
            )
            paypal_subscription = get_subscription(billing_agreement_id)
            if subscription and paypal_subscription:
                renew_subscription(
                    subscription,
                    paypal_subscription.billing_info.next_billing_time,
                )
                return HttpResponse.status_code
        except Exception as error:
            logger.error(error)
            return HttpResponseBadRequest.status_code
    return HttpResponseBadRequest.status_code

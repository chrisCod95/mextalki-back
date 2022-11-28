import logging
from datetime import datetime

from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone

from src.mextalki.models import StripePayment
from src.subscription.models import Subscription
from src.subscription.utils import renew_subscription

logger = logging.getLogger('django')


def invoice_paid(payload):
    stripe_subscription = _get_subscription(payload)
    end_date = _get_end_date(stripe_subscription)
    subscription: Subscription = _get_subscription_by_strip_id(payload['subscription'])
    if subscription:
        renew_subscription(subscription, end_date or timezone.now())
        subscription.save()
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    stripe_payment = StripePayment(
        id=payload['id'],
        customer_id=payload['customer'],
        charge_id=payload['charge'],
        subscription_id=payload['subscription'],
        billing_reason=payload['billing_reason'],
        currency=payload.get('currency', '').upper(),
        customer_email=payload['customer_email'],
        customer_name=payload['customer_name'],
        customer_phone=payload['customer_phone'],
        invoice_pdf=payload['invoice_pdf'],
        payment_intent=payload['payment_intent'],
        status=payload['status'],
        created_at=datetime.fromtimestamp(payload['created']),
        updated_at=timezone.now(),
    )
    stripe_payment.save()
    return status_code


def invoice_payment_failed(payload):
    subscription: Subscription = _get_subscription_by_strip_id(payload['subscription'])
    if subscription:
        subscription.status = Subscription.EXPIRED
        subscription.active = False
        subscription.save()
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    return status_code


def _get_subscription_by_strip_id(stripe_subscription_id: str):

    try:
        if stripe_subscription_id is None:
            raise Exception('stripe_subscription_id is null')
        return Subscription.objects.get(provider_id=stripe_subscription_id)
    except(Exception, Subscription.DoesNotExist):
        return None


def _get_subscription(payload):
    try:
        return payload['lines']['data'][0]
    except IndexError as error:
        logger.error(error)
        return None


def _get_end_date(stripe_subscription):
    if stripe_subscription:
        return datetime.fromtimestamp(stripe_subscription['period']['end'])
    return None

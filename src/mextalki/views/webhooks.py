import json
import logging
import time
from types import MappingProxyType

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from src.mextalki.paypal import webhooks as paypal_webhooks
from src.mextalki.stripe import webhooks as stripe_webhooks
from src.mextalki.utils import get_request_payload
from src.mextalki.zapier import webhooks as zapier_webhooks

logger = logging.getLogger('django')


PAYPAL_EVENT_TYPES = MappingProxyType({
    'BILLING.SUBSCRIPTION.ACTIVATED': paypal_webhooks.process_subscription_activated,
    'BILLING.SUBSCRIPTION.CANCELLED': paypal_webhooks.process_subscription_cancelled,
    'BILLING.SUBSCRIPTION.CREATED': paypal_webhooks.process_subscription_created,
    'BILLING.SUBSCRIPTION.EXPIRED': paypal_webhooks.process_subscription_expired,
    'BILLING.SUBSCRIPTION.PAYMENT.FAILED': paypal_webhooks.process_subscription_payment_failed,
    'BILLING.SUBSCRIPTION.RE-ACTIVATED': paypal_webhooks.process_subscription_re_activated,
    'BILLING.SUBSCRIPTION.RENEWED': paypal_webhooks.process_subscription_renewed,
    'BILLING.SUBSCRIPTION.SUSPENDED': paypal_webhooks.process_subscription_suspended,
    'BILLING.SUBSCRIPTION.UPDATED': paypal_webhooks.process_subscription_updated,
    'PAYMENT.SALE.COMPLETED': paypal_webhooks.payment_sale_completed,
})

STRIPE_EVENT_TYPES = MappingProxyType({
    'invoice.paid': stripe_webhooks.invoice_paid,
    'invoice.payment_failed': stripe_webhooks.invoice_payment_failed,
})

ZAPIER_EVENT_TYPES = MappingProxyType({
    'event.scheduled': zapier_webhooks.process_scheduled_event,
    'event.canceled': zapier_webhooks.process_canceled_event,
})


@csrf_exempt
@require_http_methods(['POST'])
def paypal_webhook_view(request):
    try:
        time.sleep(3)
        payload = get_request_payload(request)
        event_type = payload.get('event_type')
        resource = payload.get('resource')
        processor = PAYPAL_EVENT_TYPES[event_type]
        status_code = processor(resource)
    except (NotImplementedError, KeyError):
        status_code = HttpResponseBadRequest.status_code
    except json.JSONDecodeError:
        status_code = HttpResponseBadRequest.status_code
    return HttpResponse(status=status_code)


@csrf_exempt
@require_http_methods(['POST'])
def stripe_webhook_view(request):
    try:
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.body,
                sig_header=signature,
                secret=settings.STRIPE_WEBHOOK_SECRET,
                api_key=settings.STRIPE_SECRET_KEY,
            )
            payload = event['data']
            event_type = event['type']
        except Exception as error:
            logger.error(error)
            request_data = get_request_payload(request)
            payload = request_data['data']
            event_type = request_data['type']
        processor = STRIPE_EVENT_TYPES[event_type]
        status_code = processor(payload.get('object'))
    except (NotImplementedError, KeyError):
        status_code = HttpResponse.status_code
    except json.JSONDecodeError:
        status_code = HttpResponseBadRequest.status_code
    return JsonResponse(
        {'status': 'success'},
        status=status_code,
    )


@csrf_exempt
@require_http_methods(['POST'])
def zapier_webhook_view(request):
    try:
        time.sleep(3)
        payload = get_request_payload(request)
        event_type = payload.get('event_type')
        processor = ZAPIER_EVENT_TYPES[event_type]
        status_code = processor(payload)
    except (NotImplementedError, KeyError):
        status_code = HttpResponse.status_code
    return JsonResponse(
        {'status': 'success'},
        status=status_code,
    )

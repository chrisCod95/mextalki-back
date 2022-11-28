from typing import Callable, Optional

from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse, QueryDict
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from src.mextalki.logger import logger
from src.mextalki.stripe import (
    create_checkout_session,
    create_subscription_checkout_session,
)
from src.mextalki.utils import get_request_payload
from src.subscription.models import SubscriptionType
from src.users.models import User


@csrf_protect
@require_http_methods(['POST'])
def stripe_create_subscription_checkout_session_view(request):
    payload = get_request_payload(request)
    user: User = request.user
    price_id = payload['price_id']
    subscription_type: SubscriptionType = _get_subscription_by_stripe_price_id(
        price_id,
    )
    if subscription_type:
        cancel_url = request.build_absolute_uri(
            reverse('subscription'),
        )
        success_url = _build_subscription_success_url(
            build_absolute_uri=request.build_absolute_uri,
            user_uid=user.uid,
            subscription_uid=subscription_type.uid,
        )
        try:
            checkout_session = create_subscription_checkout_session(
                price_id,
                success_url,
                cancel_url,
            )
            return JsonResponse(
                {
                    'sessionId': checkout_session['id'],
                },
            )
        except Exception as error:
            return JsonResponse(
                {
                    'error': {
                        'message': str(error),
                    },
                },
                status=HttpResponseBadRequest.status_code,
            )
    return JsonResponse(
        {
            'error': {
                'message': 'subscription does not exist',
            },
        },
        status=HttpResponseBadRequest.status_code,
    )


@csrf_protect
@require_http_methods(['POST'])
def stripe_create_extra_seats_session_view(request):
    payload = get_request_payload(request)
    user = request.user
    price = _format_stripe_price(payload['price'])
    product: str = payload['product']
    seats = payload['seats']
    user_credits = payload.get('credits')
    referer = request.META.get('HTTP_REFERER')
    success_url = _build_extra_seats_success_url(
        build_absolute_uri=request.build_absolute_uri,
        user_uid=user.uid,
        seats=seats,
        user_credits=user_credits,
    )
    try:
        checkout_session = create_checkout_session(
            price,
            product.upper(),
            success_url,
            referer,
        )
        return JsonResponse(
            {
                'sessionId': checkout_session['id'],
            },
        )
    except Exception as error:
        return JsonResponse(
            {
                'error': {
                    'message': str(error),
                },
            },
            status=HttpResponseBadRequest.status_code,
        )


@csrf_protect
@require_http_methods(['POST'])
def stripe_create_checkout_session_view(request):
    payload = get_request_payload(request)
    user = request.user
    price = _format_stripe_price(payload['price'])
    product: str = payload['product']
    hours = payload['hours']
    event_type = payload['event_type']
    coupon_code = payload.get('coupon_code')
    user_credits = payload.get('credits')
    referer = request.META.get('HTTP_REFERER')
    success_url = _build_extra_lesson_success_url(
        build_absolute_uri=request.build_absolute_uri,
        user_uid=user.uid,
        hours=hours,
        event_type=event_type,
        coupon_code=coupon_code,
        user_credits=user_credits,
    )
    try:
        checkout_session = create_checkout_session(
            price,
            product.upper(),
            success_url,
            referer,
        )
        return JsonResponse(
            {
                'sessionId': checkout_session['id'],
            },
        )
    except Exception as error:
        return JsonResponse(
            {
                'error': {
                    'message': str(error),
                },
            },
            status=HttpResponseBadRequest.status_code,
        )


def _set_message_success(request, message):
    messages.success(request, message)


def _set_message_error(request, message):
    messages.error(request, message)


def _get_subscription_by_stripe_price_id(price_id):
    try:
        return SubscriptionType.objects.get(stripe_price_id=price_id)
    except SubscriptionType.DoesNotExist as error:
        logger.error(error)
        return None


def _build_subscription_success_url(build_absolute_uri: Callable, user_uid: str, subscription_uid: str):
    return '{url}?session_id={{CHECKOUT_SESSION_ID}}'.format(
        url=build_absolute_uri(
            reverse(
                'process_stripe_subscription_payment',
                kwargs={
                    'user_uid_b64': user_uid,
                    'subscription_uid_b64': subscription_uid,
                },
            ),
        ),
    )


def _build_extra_seats_success_url(build_absolute_uri: Callable, user_uid: str, seats, user_credits: Optional[str] = None):
    base_url = '{url}?session_id={{CHECKOUT_SESSION_ID}}'.format(
        url=build_absolute_uri(
            reverse(
               'process_stripe_extra_seats_payment',
                kwargs={
                    'user_uid_b64': user_uid,
                    'seats': seats,
                },
            ),
        ),
    )
    if user_credits:
        query_dictionary = QueryDict('', mutable=True)
        query_dictionary.update({'credits': user_credits})
        return '{base_url}&{querystring}'.format(
            base_url=base_url,
            querystring=query_dictionary.urlencode(),
        )
    return base_url


def _build_extra_lesson_success_url(
    build_absolute_uri: Callable,
    user_uid: str, hours,
    event_type: str,
    coupon_code: Optional[str] = None,
    user_credits: Optional[str] = None,
):
    base_url = '{url}?session_id={{CHECKOUT_SESSION_ID}}'.format(
        url=build_absolute_uri(
            reverse(
                'process_stripe_extra_hours_payment',
                kwargs={
                    'user_uid_b64': user_uid,
                    'hours': hours,
                    'event_type': event_type,
                },
            ),
        ),
    )
    if not coupon_code and not user_credits:
        return base_url
    query_dictionary = QueryDict('', mutable=True)
    if coupon_code:
        query_dictionary.update({'coupon_code': coupon_code})

    if user_credits:
        query_dictionary.update({'credits': user_credits})

    return '{base_url}&{querystring}'.format(
        base_url=base_url,
        querystring=query_dictionary.urlencode(),
    )


def _format_stripe_price(price: str):
    return '{:.2f}'.format(float(price)).replace('.', '')

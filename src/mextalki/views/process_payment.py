from json import loads

from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from src.mextalki.stripe import retrieve_checkout_session
from src.mextalki.utils import (
    set_used_coupon,
    set_used_credits,
    get_user_by_uid,
    redeem_purchased_conversation_club_seats,
    redeem_purchased_lesson_hours,
    redeem_purchased_practice_hours,
    send_purchase_hours_email,
)
from src.mextalki.views.constants import BUY_EXTRA_LESSON_EVENT_TYPES
from src.subscription.models import Subscription
from src.subscription.utils import (
    create_subscription,
    get_subscription_type_by_uid,
    send_subscription_message,
)
from src.users.models import User
from src.users.utils.update_referral import update_referral_subscription


@csrf_protect
@require_http_methods(['POST'])
def process_swap_credits_view(request, user_uid_b64, event_type):
    if event_type not in BUY_EXTRA_LESSON_EVENT_TYPES.values():
        raise Http404()
    if not request.is_ajax():
        raise Http404()
    user = get_user_by_uid(user_uid_b64)
    if user:
        payload: dict = loads(request.body.decode('utf-8'))
        if event_type == BUY_EXTRA_LESSON_EVENT_TYPES['CONVERSATION_CLUB']:
            redeem_purchased_conversation_club_seats(
                user=user,
                purchased_seats=payload['purchased_seats'],
            )
        if event_type == BUY_EXTRA_LESSON_EVENT_TYPES['LESSON']:
            redeem_purchased_lesson_hours(
                user=user,
                purchased_hours=payload['purchased_hours'],
            )
        elif event_type == BUY_EXTRA_LESSON_EVENT_TYPES['PRACTICE']:
            redeem_purchased_practice_hours(
                user=user,
                purchased_hours=payload['purchased_hours'],
            )
        set_used_credits(
            user=user,
            user_credits=payload['credits'],
        )
        status_code = HttpResponse.status_code
        _set_message_success(
            request,
            'Congratulations your swap was processed correctly.',
        )
    else:
        status_code = HttpResponseBadRequest.status_code
        _set_message_error(
            request,
            'Sorry your swap was not processed correctly, try again.',
        )
    response = {
        'status': status_code,
        'redirect_url': reverse_lazy('dashboard'),
    }
    return JsonResponse(response, status=status_code)


def process_stripe_subscription_view(request, user_uid_b64, subscription_uid_b64):
    user = get_user_by_uid(user_uid_b64)
    subscription_type = get_subscription_type_by_uid(subscription_uid_b64)
    session_id = _get_session_id(request)
    stripe_session = retrieve_checkout_session(session_id)
    subscription = create_subscription(
        user=user,
        subscription_type=subscription_type,
        provider=Subscription.STRIPE,
        provider_id=stripe_session.get('subscription'),
    )
    send_subscription_message(subscription, subscription_type, user)
    update_referral_subscription(user, subscription_type)
    return redirect(reverse_lazy('subscription_confirmation'))


def process_stripe_extra_seats_payment_view(request, user_uid_b64, seats):
    user: User = get_user_by_uid(user_uid_b64)
    user_credits = request.GET.get('credits')
    session_id = _get_session_id(request)
    if user and session_id:
        retrieve_checkout_session(session_id)
        redeem_purchased_conversation_club_seats(
            user=user,
            purchased_seats=seats,
        )
        _set_message_success(
            request,
            'Congratulations your payment was processed correctrly.',
        )
        if user_credits:
            set_used_credits(user, user_credits)
    else:
        _set_message_error(
            request,
            'Sorry your payment was not processed correctly, try again.',
        )
    return redirect(reverse_lazy('conversation_club'))


def process_stripe_extra_hour_payment_view(request, user_uid_b64, hours, event_type):
    user: User = get_user_by_uid(user_uid_b64)
    session_id = _get_session_id(request)
    coupon_code = request.GET.get('coupon_code')
    user_credits = request.GET.get('credits')
    if user and session_id:
        retrieve_checkout_session(session_id)
        if event_type == BUY_EXTRA_LESSON_EVENT_TYPES['LESSON']:
            redeem_purchased_lesson_hours(
                user=user,
                purchased_hours=hours,
            )
        elif event_type == BUY_EXTRA_LESSON_EVENT_TYPES['PRACTICE']:
            redeem_purchased_practice_hours(
                user=user,
                purchased_hours=hours,
            )
        send_purchase_hours_email(
            user=user,
            purchased_hours=hours,
            event_type=event_type,
        )
        _set_message_success(
            request,
            'Congratulations your payment was processed correctly.',
        )
        if coupon_code:
            set_used_coupon(user, coupon_code)
        if user_credits:
            set_used_credits(user, user_credits)
    else:
        _set_message_error(
            request,
            'Sorry your payment was not processed correctly, try again.',
        )
    return redirect(reverse_lazy('dashboard'))


def _set_message_success(request, message):
    messages.success(request, message)


def _set_message_error(request, message):
    messages.error(request, message)


def _get_session_id(request):
    return request.GET.get('session_id')

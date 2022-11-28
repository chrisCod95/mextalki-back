from json import JSONDecodeError, loads
from time import sleep

from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods

from src.mextalki.utils import (
    get_plan_by_uid,
    get_user_by_uid,
    redeem_purchased_conversation_club_seats,
    redeem_purchased_lesson_hours,
    redeem_purchased_practice_hours,
    send_purchase_hours_email,
    set_used_coupon,
    set_used_credits,
)
from src.mextalki.views.constants import BUY_EXTRA_LESSON_EVENT_TYPES
from src.paypal.logger import logger
from src.paypal.utils import create_paypal_payment, create_plan_payment
from src.paypal.webhooks import PAYPAL_EVENT_TYPES
from src.subscription.models import Subscription
from src.subscription.utils import (
    create_subscription,
    get_subscription_type_by_uid,
    send_subscription_message,
)
from src.users.utils.update_referral import update_referral_subscription


@csrf_exempt
@require_http_methods(['POST'])
def paypal_webhook_view(request):
    try:
        payload: dict = loads(request.body.decode('utf-8'))
        logger.info(payload)
        sleep(3)
        event_type = payload.get('event_type')
        resource = payload.get('resource')
        processor = PAYPAL_EVENT_TYPES[event_type]
        status_code = processor(resource)
    except (NotImplementedError, KeyError):
        status_code = HttpResponseBadRequest.status_code
    except JSONDecodeError:
        status_code = HttpResponseBadRequest.status_code
    return HttpResponse(status=status_code)


@csrf_protect
@require_http_methods(['POST'])
def process_paypal_plan_payment_view(request, user_uid_b64, plan_uid_b64):
    if request.is_ajax():
        user = get_user_by_uid(user_uid_b64)
        plan = get_plan_by_uid(plan_uid_b64)
        redirect_url = reverse_lazy('dashboard')
        if user and plan:
            paypal_payload = loads(request.body.decode('utf-8'))
            paypal_payment = create_paypal_payment(paypal_payload)
            create_plan_payment(user, plan, paypal_payment)
            status_code = HttpResponse.status_code
            _set_message_success(
                request,
                'Congratulations your payment was processed correctly, now you can access to {course}'.format(
                    course=plan.course.title,
                ),
            )
        else:
            status_code = HttpResponseBadRequest.status_code
            _set_message_error(
                request,
                'Sorry your payment was not processed correctly, try again.',
            )
        response = {
            'status': status_code,
            'redirect_url': redirect_url,
        }
        return JsonResponse(response, status=status_code)
    return redirect(reverse_lazy('index'))


@csrf_protect
@require_http_methods(['POST'])
def process_paypal_extra_hours_payment_view(request, user_uid_b64, event_type):
    if event_type not in BUY_EXTRA_LESSON_EVENT_TYPES.values():
        raise Http404()
    if not request.is_ajax():
        raise Http404()
    user = get_user_by_uid(user_uid_b64)
    redirect_url = reverse_lazy('dashboard')
    if user:
        paypal_payload: dict = loads(request.body.decode('utf-8'))
        create_paypal_payment(paypal_payload)
        if event_type == BUY_EXTRA_LESSON_EVENT_TYPES['LESSON']:
            redeem_purchased_lesson_hours(
                user=user,
                purchased_hours=paypal_payload['purchased_hours'],
            )
        elif event_type == BUY_EXTRA_LESSON_EVENT_TYPES['PRACTICE']:
            redeem_purchased_practice_hours(
                user=user,
                purchased_hours=paypal_payload['purchased_hours'],
            )
        send_purchase_hours_email(
            user=user,
            purchased_hours=paypal_payload['purchased_hours'],
            event_type=event_type,
        )
        coupon_code = paypal_payload.get('coupon_code')
        user_credits = paypal_payload.get('credits')
        if coupon_code:
            set_used_coupon(user, coupon_code)
        if user_credits:
            set_used_credits(user, user_credits)
        status_code = HttpResponse.status_code
        _set_message_success(
            request,
            'Congratulations your payment was processed correctly.',
        )
    else:
        status_code = HttpResponseBadRequest.status_code
        _set_message_error(
            request,
            'Sorry your payment was not processed correctly, try again.',
        )
    response = {
        'status': status_code,
        'redirect_url': redirect_url,
    }
    return JsonResponse(response, status=status_code)


@csrf_protect
@require_http_methods(['POST'])
def process_paypal_subscription_payment_view(request, user_uid_b64, subscription_uid_b64):
    if request.is_ajax():
        user = get_user_by_uid(user_uid_b64)
        subscription_type = get_subscription_type_by_uid(subscription_uid_b64)
        redirect_url = reverse_lazy('subscription_confirmation')
        if user and subscription_type:
            paypal_payload: dict = loads(request.body.decode('utf-8'))
            subscription = create_subscription(
                user=user,
                subscription_type=subscription_type,
                provider=Subscription.PAYPAL,
                provider_id=paypal_payload['paypal_subscription_id'],
            )
            send_subscription_message(subscription, subscription_type, user)
            update_referral_subscription(user, subscription_type)
            status_code = HttpResponse.status_code
        else:
            status_code = HttpResponseBadRequest.status_code
        response = {
            'status': status_code,
            'redirect_url': redirect_url,
        }
        return JsonResponse(response, status=status_code)
    return redirect(reverse_lazy('index'))


@csrf_protect
@require_http_methods(['POST'])
def process_paypal_extra_seats_payment_view(request, user_uid_b64):
    if not request.is_ajax():
        raise Http404()
    user = get_user_by_uid(user_uid_b64)
    redirect_url = reverse_lazy('conversation_club')
    if user:
        paypal_payload: dict = loads(request.body.decode('utf-8'))
        user_credits = paypal_payload.get('credits')
        create_paypal_payment(paypal_payload)
        redeem_purchased_conversation_club_seats(
            user=user,
            purchased_seats=paypal_payload['purchased_seats'],
        )
        status_code = HttpResponse.status_code
        _set_message_success(
            request,
            'Congratulations your payment was processed correctly.',
        )
        if user_credits:
            set_used_credits(user, user_credits)
    else:
        status_code = HttpResponseBadRequest.status_code
        _set_message_error(
            request,
            'Sorry your payment was not processed correctly, try again.',
        )
    response = {
        'status': status_code,
        'redirect_url': redirect_url,
    }
    return JsonResponse(response, status=status_code)


def _set_message_success(request, message):
    messages.success(request, message)


def _set_message_error(request, message):
    messages.error(request, message)

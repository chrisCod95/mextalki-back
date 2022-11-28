from django.urls import path

from src.paypal.views import (
    paypal_webhook_view,
    process_paypal_extra_hours_payment_view,
    process_paypal_extra_seats_payment_view,
    process_paypal_plan_payment_view,
    process_paypal_subscription_payment_view,
)

urlpatterns = [
    path(
        'webhook/',
        paypal_webhook_view,
        name='paypal_webhook',
    ),
    path(
        'plan/success/<str:user_uid_b64>/<str:plan_uid_b64>/',
        process_paypal_plan_payment_view,
        name='process_paypal_plan_payment',
    ),
    path(
        'subscription/success/<str:user_uid_b64>/<str:subscription_uid_b64>/',
        process_paypal_subscription_payment_view,
        name='process_paypal_subscription_payment',
    ),
    path(
        'extra_hours/success/<str:user_uid_b64>/<str:event_type>/',
        process_paypal_extra_hours_payment_view,
        name='process_paypal_extra_hours_payment',
    ),
    path(
        'extra_seats/success/<str:user_uid_b64>/',
        process_paypal_extra_seats_payment_view,
        name='process_paypal_extra_seats_payment',
    ),
]

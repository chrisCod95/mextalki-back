from django.urls import path

from src.subscription.views import (
    CancelSubscriptionView,
    NewSubscriptionView,
    SubscriptionConfirmationView, SubscriptionTest,
)

urlpatterns = [
    path(
        '',
        NewSubscriptionView.as_view(),
        name='subscription',
    ),
    path(
        'cancel',
        CancelSubscriptionView.as_view(),
        name='cancel_subscription',
    ),
    path(
        'confirmation',
        SubscriptionConfirmationView.as_view(),
        name='subscription_confirmation',
    ),
    path(
        'subscription-test',
        SubscriptionTest.as_view(),
        name='subscription_test',
    ),
]

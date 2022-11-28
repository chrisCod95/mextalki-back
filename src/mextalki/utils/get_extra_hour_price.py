from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model

from src.mextalki.views.constants import BUY_EXTRA_LESSON_EVENT_TYPES
from src.subscription.models import SubscriptionType

UserModel = get_user_model()


def get_subscription_type(user: UserModel) -> Optional[SubscriptionType]:
    last_subscription = user.last_subscription
    if last_subscription:
        return last_subscription.subscription_type
    return None


def get_extra_hour_price(user: UserModel, event_type: str):
    subscription_type: Optional[SubscriptionType] = get_subscription_type(user=user)
    if event_type == BUY_EXTRA_LESSON_EVENT_TYPES['PRACTICE']:
        if subscription_type:
            return subscription_type.extra_hour_practice_price
        return settings.EXTRA_HOUR_PRACTICE_BASE_PRICE
    if event_type == BUY_EXTRA_LESSON_EVENT_TYPES['LESSON']:
        if subscription_type:
            return subscription_type.extra_hour_lesson_price
        return settings.EXTRA_HOUR_LESSON_BASE_PRICE

    if event_type == BUY_EXTRA_LESSON_EVENT_TYPES['CONVERSATION_CLUB']:
        if subscription_type:
            return settings.EXTRA_SEAT_CONVO_CLUB_WITH_SUBSCRIPTION_PRICE
        return settings.EXTRA_SEAT_CONVO_CLUB_BASE_PRICE


def get_extra_hour_info(user: UserModel):
    subscription_type: Optional[SubscriptionType] = get_subscription_type(user=user)
    extra_hour_currency = settings.EXTRA_HOUR_CURRENCY
    extra_hour_title = None
    extra_hour_color = None
    if subscription_type:
        extra_hour_currency = subscription_type.extra_hour_currency
        extra_hour_title = subscription_type.title
        extra_hour_color = '#251182'
    return extra_hour_currency, extra_hour_title, extra_hour_color

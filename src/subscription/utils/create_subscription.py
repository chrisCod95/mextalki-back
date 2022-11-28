from datetime import timedelta

from django.utils import timezone

from src.subscription.models import Subscription, SubscriptionType


def create_subscription(user, subscription_type: SubscriptionType, provider: str, provider_id=None):
    subscription = Subscription(
        user=user,
        subscription_type=subscription_type,
        provider=provider,
        next_billing_time=timezone.now() + timedelta(days=1),
        provider_id=provider_id,
    )
    user.set_conversation_club_slots(subscription_type.conversation_club_slots)
    user.add_available_lesson_time(subscription_type.lesson_time_in_minutes)
    user.add_available_practice_time(subscription_type.practice_time_in_minutes)
    subscription.save()
    return subscription

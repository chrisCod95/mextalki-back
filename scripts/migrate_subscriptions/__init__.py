import logging
from typing import Optional

from src.mextalki.models import SubscriptionType, Subscription
from src.subscription.models import SubscriptionType as NewSubscriptionType, Subscription as NewSubscription

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


def run():
    subscriptions = Subscription.objects.all()

    subscription: Subscription
    for subscription in subscriptions:
        new_type = get_new_subscription_type(subscription.subscription_type)
        if not new_type:
            continue
        new_subscription = NewSubscription(
            id=subscription.id,
            user=subscription.user,
            active=subscription.active,
            next_billing_time=subscription.next_billing_time,
            provider=subscription.provider,
            provider_id=subscription.provider_id,
            subscription_type=new_type,
        )
        new_subscription.save()


def get_new_subscription_type(old_type: SubscriptionType) -> Optional[NewSubscriptionType]:
    try:
        return NewSubscriptionType.objects.get(title=old_type.title)
    except NewSubscriptionType.DoesNotExist:
        logger.error('can find new type: {type}'.format(type=old_type.title))
        return None

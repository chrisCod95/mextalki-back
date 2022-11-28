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
        new_subscription = NewSubscription.objects.get(id=subscription.id)
        new_subscription.status = subscription.status
        new_subscription.save()


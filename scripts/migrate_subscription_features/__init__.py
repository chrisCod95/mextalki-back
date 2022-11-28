import logging
from typing import Optional

from src.mextalki.models import SubscriptionType, SubscriptionFeature
from src.subscription.models import SubscriptionType as NewSubscriptionType, SubscriptionFeature as NewSubscriptionFeature

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


def run():
    subscriptions_features = SubscriptionFeature.objects.all().order_by('id')
    for subscriptions_feature in subscriptions_features:
        new_feature = NewSubscriptionFeature(
            feature=subscriptions_feature.feature,
            subscription_type=get_new_subscription_type(subscriptions_feature.subscription_type),
        )
        new_feature.save()


def get_new_subscription_type(old_type: SubscriptionType) -> Optional[NewSubscriptionType]:
    try:
        return NewSubscriptionType.objects.get(title=old_type.title)
    except NewSubscriptionType.DoesNotExist:
        logger.error('can find new type: {type}'.format(type=old_type.title))
        return None


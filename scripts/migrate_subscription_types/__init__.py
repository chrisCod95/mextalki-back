import logging
from src.mextalki.models import SubscriptionType
from src.subscription.models import SubscriptionType as NewSubscriptionType

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


def run():
    subscriptions_types = SubscriptionType.objects.all().order_by('id')
    for subscription_type in subscriptions_types:
        new_type = NewSubscriptionType(
            title=subscription_type.title,
            price=subscription_type.price,
            currency=subscription_type.currency,
            active=subscription_type.active,
            color=subscription_type.color,
            billing_cycle=subscription_type.billing_cycle,
            paypal_plan_id=subscription_type.paypal_plan_id,
            stripe_price_id=subscription_type.stripe_price_id,
            lesson_time=subscription_type.lesson_time,
            practice_time=subscription_type.practice_time,
            extra_hour_lesson_price=subscription_type.extra_hour_lesson_price,
            extra_hour_practice_price=subscription_type.extra_hour_practice_price,
            extra_hour_currency=subscription_type.extra_hour_currency,
            conversation_club_slots=subscription_type.conversation_club_slots,
            has_access_to_courses=subscription_type.has_access_to_courses,
            include_basic_package=subscription_type.include_basic_package,
            include_conversation_club=subscription_type.include_conversation_club,
            include_podcast_features=subscription_type.include_podcast_features,
        )
        new_type.save()


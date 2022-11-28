from django.utils import timezone

from src.aws import SEND_NOTIFICATION_EMAIL_QUEUE_URL, enqueue
from src.subscription.logger import logger
from src.subscription.models import Subscription, SubscriptionType


def send_subscription_renew_message(subscription_type: SubscriptionType, user):
    try:
        enqueue(
            SEND_NOTIFICATION_EMAIL_QUEUE_URL,
            {
                'email_type': 'RENEW_SUBSCRIPTION',
                'destination': user.email,
                'replacements': {
                    'user_name': user.username,
                    'subscription_type': subscription_type.title,
                    'price': '${price} {currency}'.format(
                        price=subscription_type.price,
                        currency=subscription_type.currency,
                    ),
                    'payment_date': timezone.now().strftime('%d/%m/%Y'),
                },
            },
        )
    except Exception as error:
        logger.error(error)


def renew_subscription(subscription: Subscription, next_billing_time):
    subscription.status = Subscription.ACTIVE
    subscription.active = True
    subscription.next_billing_time = next_billing_time
    subscription.user.set_available_lesson_time(
        subscription.subscription_type.lesson_time_in_minutes,
    )
    subscription.user.set_conversation_club_slots(
        subscription.subscription_type.conversation_club_slots,
    )
    subscription.user.set_available_practice_time(
        subscription.subscription_type.practice_time_in_minutes,
    )
    send_subscription_renew_message(
        subscription_type=subscription.subscription_type,
        user=subscription.user,
    )
    return subscription.save()

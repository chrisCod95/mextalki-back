from src.aws import SEND_NOTIFICATION_EMAIL_QUEUE_URL, enqueue
from src.subscription.logger import logger
from src.subscription.models import Subscription, SubscriptionType


def send_subscription_message(
    subscription: Subscription,
    subscription_type: SubscriptionType,
    user,
):
    try:
        enqueue(
            SEND_NOTIFICATION_EMAIL_QUEUE_URL,
            {
                'email_type': 'START_SUBSCRIPTION',
                'destination': user.email,
                'replacements': {
                    'user_name': user.username,
                    'subscription_type': subscription_type.title,
                    'price': '${price} {currency}'.format(
                        price=subscription_type.price,
                        currency=subscription_type.currency,
                    ),
                    'due_date': subscription.next_billing_time.strftime('%d/%m/%Y'),
                },
            },
        )
    except Exception as error:
        logger.error(error)

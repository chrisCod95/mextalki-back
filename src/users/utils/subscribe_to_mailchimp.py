from src.aws import SUBSCRIBE_MAILCHIMP_USER_QUEUE_URL, enqueue
from src.mextalki.logger import logger


def subscribe_mailchimp_user(user):
    try:
        enqueue(
            SUBSCRIBE_MAILCHIMP_USER_QUEUE_URL,
            {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
        )
    except Exception as error:
        logger.error(error)

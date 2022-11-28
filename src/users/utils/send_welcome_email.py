from src.aws import SEND_NOTIFICATION_EMAIL_QUEUE_URL, enqueue
from src.mextalki.logger import logger


def send_welcome_email(user):
    try:
        enqueue(
            SEND_NOTIFICATION_EMAIL_QUEUE_URL,
            {
                'email_type': 'WELCOME_EMAIL',
                'destination': user.email,
                'replacements': {
                    'user_name': user.username,
                },
            },
        )
    except Exception as error:
        logger.error(error)

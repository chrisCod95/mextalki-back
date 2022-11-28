from django.utils import timezone

from src.aws import SEND_NOTIFICATION_EMAIL_QUEUE_URL, enqueue
from src.mextalki.logger import logger
from src.mextalki.templatetags.duration_format import duration_format


def send_purchase_hours_email(user, purchased_hours: str, event_type: str):
    purchased_hours_in_hours = float(purchased_hours)
    time_purchased = duration_format(int(purchased_hours_in_hours * 60))
    try:
        enqueue(
            SEND_NOTIFICATION_EMAIL_QUEUE_URL,
            {
                'email_type': 'PURCHASE_HOURS',
                'destination': user.email,
                'replacements': {
                    'user_name': user.username,
                    'payment_date': timezone.now().strftime('%d/%m/%Y'),
                    'time_purchased': time_purchased,
                    'lesson_type': event_type.upper(),
                },
            },
        )
    except Exception as error:
        logger.error(error)

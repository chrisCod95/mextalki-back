from src.aws import SEND_NOTIFICATION_EMAIL_QUEUE_URL, enqueue
from src.mextalki.logger import logger
from src.mextalki.models import Reminder


def send_reminder(reminder: Reminder):
    if reminder.scheduled_event.event_type.is_conversation_club():
        body_message = {
            'email_type': 'CONVO_CLUB_REMINDER',
            'destination': reminder.user.email,
            'replacements': {
                'user_name': reminder.user.username,
                'convo_club_link': reminder.scheduled_event.location,
            },
        }
    else:
        body_message = {
            'email_type': 'LESSON_REMINDER',
            'destination': reminder.user.email,
            'replacements': {
                'user_name': reminder.user.username,
                'time_until_lesson': '60',
                'teacher_name': reminder.scheduled_event.teacher.name,
                'lesson_link': reminder.scheduled_event.location,
            },
        }
    try:
        enqueue(
            SEND_NOTIFICATION_EMAIL_QUEUE_URL,
            body_message,
        )
    except Exception as error:
        logger.error(error)

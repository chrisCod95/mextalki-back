from datetime import datetime, timedelta

from celery import shared_task

from src.mextalki.logger import logger
from src.mextalki.models import Reminder
from src.mextalki.utils import send_reminder


@shared_task
def reminders_monitor(*args, **kwargs):
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=30)
    logger.info('start_time: %s', start_time.isoformat())
    logger.info('end_time: %s', end_time.isoformat())
    reminders = Reminder.objects.filter(
        reminder_schedule__range=(start_time, end_time),
        reminder_was_sent=False,
        event_status=Reminder.ACTIVE,
    )
    logger.info('reminders count: %s', reminders.count())
    logger.info(reminders)
    for reminder in reminders:
        send_reminder(reminder)
        reminder.reminder_was_sent = True
        reminder.save()

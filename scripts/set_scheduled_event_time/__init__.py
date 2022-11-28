import logging
from src.mextalki.models import ScheduledEvent

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


def run():
    scheduled_events = ScheduledEvent.objects.filter(status=ScheduledEvent.ACTIVE)
    for scheduled_event in scheduled_events:
        scheduled_event.scheduled_with_subscription_time = scheduled_event.event_type.event_duration
        scheduled_event.save()

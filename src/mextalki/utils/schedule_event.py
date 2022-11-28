import datetime

from src.mextalki.models import EventType, Reminder, ScheduledEvent, Teacher
from src.users.models import User


def create_event_reminder(user: User, event: ScheduledEvent):
    reminder = Reminder(
        user=user,
        scheduled_event=event,
        event_status=Reminder.ACTIVE,
        reminder_schedule=(event.start_time - datetime.timedelta(minutes=60)),
    )
    reminder.save()
    return reminder


def cancel_event_reminder(event: ScheduledEvent):
    for reminder in event.reminders.all():
        reminder.event_status = Reminder.CANCELLED
        reminder.save()


def create_scheduled_event(
    user: User,
    event_type: EventType,
    teacher: Teacher,
    provider: str,
    provider_event_id: str,
    provider_invite_id: str,
):
    scheduled_with_subscription_time, scheduled_with_purchased_time = get_scheduled_times(
        event_type, user,
    )

    scheduled_event = ScheduledEvent(
        user=user,
        event_type=event_type,
        teacher=teacher,
        provider=provider,
        provider_event_id=provider_event_id,
        provider_invite_id=provider_invite_id,
        scheduled_with_subscription_time=scheduled_with_subscription_time,
        scheduled_with_purchased_time=scheduled_with_purchased_time,
    )
    scheduled_event.save()
    if event_type.is_conversation_club():
        remove_slots(user)
    else:
        remove_hours(
            event_type, user, scheduled_with_subscription_time,
            scheduled_with_purchased_time,
        )
    return scheduled_event


def get_scheduled_times(event_type: EventType, user: User):
    duration = event_type.event_duration
    if event_type.is_lesson():
        if user.available_lesson_time >= duration:
            return duration, 0
        return user.available_lesson_time, duration - user.available_lesson_time
    elif event_type.is_practice():
        if user.available_practice_time >= duration:
            return duration, 0
        return user.available_practice_time, duration - user.available_practice_time
    return 0, 0


def remove_slots(user: User):
    user.remove_conversation_club_slots(1)


def remove_hours(event_type: EventType, user: User, scheduled_with_subscription_time, scheduled_with_purchased_time):
    if event_type.is_lesson():
        user.remove_available_lesson_time(scheduled_with_subscription_time)
        user.remove_purchased_lesson_time(scheduled_with_purchased_time)
    elif event_type.is_practice():
        user.remove_available_practice_time(scheduled_with_subscription_time)
        user.remove_purchased_practice_time(scheduled_with_purchased_time)

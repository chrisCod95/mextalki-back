from django.contrib.auth import get_user_model

from src.mextalki.logger import logger
from src.mextalki.models import EventType, ScheduledEvent

UserModel = get_user_model()


def return_event_time_or_slot(scheduled_event: ScheduledEvent, user: UserModel):
    event_type: EventType = scheduled_event.event_type
    if event_type.is_conversation_club():
        user.add_conversation_club_slots(1)
    elif event_type.is_lesson():
        user.add_available_lesson_time(scheduled_event.scheduled_with_subscription_time)
        user.add_purchased_lesson_time(scheduled_event.scheduled_with_purchased_time)
    elif event_type.is_practice():
        user.add_available_practice_time(
            scheduled_event.scheduled_with_subscription_time,
        )
        user.add_purchased_practice_time(scheduled_event.scheduled_with_purchased_time)


def redeem_purchased_conversation_club_seats(user: UserModel, purchased_seats: str):
    user.add_purchased_conversation_club_slots(int(purchased_seats))
    logger.info(
        'user: {user_email} buy {purchased_seats} extra conversation club seats'.format(
            user_email=user.email, purchased_seats=purchased_seats,
        ),
    )
    return purchased_seats


def redeem_purchased_lesson_hours(user: UserModel, purchased_hours: str):
    purchased_hours_in_hours = float(purchased_hours)
    user.add_purchased_lesson_time(int(purchased_hours_in_hours * 60))
    logger.info(
        'user: {user_email} buy lesson {purchased_hours} hours'.format(
            user_email=user.email, purchased_hours=purchased_hours,
        ),
    )
    return purchased_hours_in_hours


def redeem_purchased_practice_hours(user: UserModel, purchased_hours: str):
    purchased_hours_in_hours = float(purchased_hours)
    user.add_purchased_practice_time(int(purchased_hours_in_hours * 60))
    logger.info(
        'user: {user_email} buy practice {purchased_hours} hours'.format(
            user_email=user.email, purchased_hours=purchased_hours,
        ),
    )
    return purchased_hours_in_hours

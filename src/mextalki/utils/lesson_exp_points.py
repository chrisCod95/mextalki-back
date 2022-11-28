from src.mextalki.models import EventType
from src.users.models import User

LESSON_EXP_POINTS = 20
PRACTICE_EXP_POINTS = 14
CONVERSATION_CLUB_EXP_POINTS = 5


def redeem_lesson_exp_points(event_type: EventType, user: User):
    points = calculate_points(event_type)
    user.add_scheduled_event_exp_points(points)
    user.leadership_board_score_sum(points, category='lesson_time')


def remove_lesson_exp_points(event_type: EventType, user: User):
    points = calculate_points(event_type)
    user.remove_scheduled_event_exp_points(points)
    user.leadership_board_score_subtract(points, category='lesson_time')


def redeem_points(duration: int, exp_points: int):
    if duration <= 30:
        return exp_points / 2
    return exp_points


def calculate_points(event_type: EventType):
    if event_type.is_lesson():
        return redeem_points(
            event_type.event_duration,
            LESSON_EXP_POINTS,
        )
    elif event_type.is_practice():
        return redeem_points(
            event_type.event_duration,
            PRACTICE_EXP_POINTS,
        )
    elif event_type.is_conversation_club():
        return CONVERSATION_CLUB_EXP_POINTS
    return 0

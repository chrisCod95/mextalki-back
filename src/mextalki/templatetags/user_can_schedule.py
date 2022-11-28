from django import template

from src.mextalki.models import EventType
from src.users.models import User

register = template.Library()


@register.filter(name='user_can_schedule')
def user_can_schedule(value: EventType, user: User) -> bool:
    if not user.is_authenticated:
        return False
    if value.is_lesson():
        return user.total_lesson_time >= value.event_duration
    if value.is_practice():
        return user.total_practice_time >= value.event_duration
    return False

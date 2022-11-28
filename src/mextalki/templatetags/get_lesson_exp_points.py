from typing import Optional

from django import template

from src.mextalki.models import Lesson, TestScore
from src.users.models import User

register = template.Library()


@register.filter(name='get_lesson_exp_points')
def get_lesson_exp_points(value: Lesson, user: User) -> Optional[int]:
    if not user.is_authenticated:
        return None
    if not value.main_test:
        return None
    try:
        return TestScore.objects.get(user=user, test=value.main_test).exp_points
    except TestScore.DoesNotExist:
        return None

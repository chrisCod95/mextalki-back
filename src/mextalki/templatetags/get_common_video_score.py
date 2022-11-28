from django import template

from src.mextalki.models import CommonVideoScore, Video
from src.users.models import User

register = template.Library()


@register.filter(name='get_common_video_score')
def get_common_video_score(value: Video, user: User) -> bool:
    if not user.is_authenticated:
        return False
    try:
        return CommonVideoScore.objects.get(user=user, video=value).user_already_get_points
    except CommonVideoScore.DoesNotExist:
        return False

from django import template

from src.mextalki.models import Podcast, VideoScore
from src.users.models import User

register = template.Library()


@register.filter(name='get_podcast_video_score')
def get_podcast_video_score(value: Podcast, user: User) -> bool:
    if not user.is_authenticated:
        return False
    try:
        return VideoScore.objects.get(user=user, podcast=value).user_already_get_points
    except VideoScore.DoesNotExist:
        return False

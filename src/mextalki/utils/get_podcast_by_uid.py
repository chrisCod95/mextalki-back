from src.mextalki.models import Podcast, VideoScore
from src.users.models import User


def get_podcast_by_uid(podcast_uid):
    try:
        return Podcast.objects.get(pk=podcast_uid)
    except Podcast.DoesNotExist:
        return None


def get_podcast_video_score_by_user(podcast: Podcast, user: User):
    try:
        return VideoScore.objects.get(user=user, podcast=podcast)
    except VideoScore.DoesNotExist:
        return VideoScore(user=user, podcast=podcast)

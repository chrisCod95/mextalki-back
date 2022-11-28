from src.mextalki.models import CommonVideoScore, Video
from src.users.models import User


def get_video_by_uid(video_uid):
    try:
        return Video.objects.get(pk=video_uid)
    except Video.DoesNotExist:
        return None


def get_video_score_by_user(video: Video, user: User):
    try:
        return CommonVideoScore.objects.get(user=user, video=video)
    except CommonVideoScore.DoesNotExist:
        return CommonVideoScore(user=user, video=video)

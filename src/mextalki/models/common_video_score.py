from django.db import models

from src.mextalki.models.base_model import TimeStampMixin


class CommonVideoScore(TimeStampMixin):

    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='common_video_scores',
    )

    video = models.ForeignKey(
        'mextalki.Video',
        on_delete=models.PROTECT,
        related_name='common_video_scores',
    )

    exp_points = models.IntegerField(default=0)

    user_already_get_points = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Scores - Videos'

    def __str__(self):
        return str(self.exp_points)

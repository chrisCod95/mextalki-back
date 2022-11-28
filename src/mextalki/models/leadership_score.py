import django
from django.db import models
from django.utils.timezone import now
from tinymce import models as tinymce_models

from src.mextalki.models.base_model import TimeStampMixin


class LeadershipBoardInfo(TimeStampMixin):
    title = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    how_get_points = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class LeadershipScore(TimeStampMixin):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='leadership_board_scores',
    )
    created_at = models.DateField(
        null=True,
        blank=True,
        default=now,
    )
    active = models.BooleanField(
        default=True,
    )
    tests_exp_points = models.IntegerField(
        default=0,
    )
    lesson_time_exp_points = models.IntegerField(
        default=0,
    )
    videos_exp_points = models.IntegerField(
        default=0,
    )
    challenges_exp_points = models.IntegerField(
        default=0,
    )
    exp_points = models.IntegerField(
        default=0,
    )

    class Meta:
        ordering = ('-exp_points',)

    def __str__(self):
        return 'user:{user} - points:{points} - {month}/{year}'.format(
            user=self.user,
            points=self.exp_points,
            month=self.created_at.month,
            year=self.created_at.year,
        )


class LeaderBoardRewards(TimeStampMixin):
    title = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    how_get_points = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Leaderboard Rewards'

    def __str__(self):
        return self.title

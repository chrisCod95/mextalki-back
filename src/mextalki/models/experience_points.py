from django.db import models

from .base_model import TimeStampMixin


class UserExperiencePoint(TimeStampMixin):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='user_experience_points',
    )

    scheduled_event_exp_points = models.IntegerField(
        default=0,
    )

    def __str__(self):
        return self.user.email

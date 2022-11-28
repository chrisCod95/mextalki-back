
from django.db import models

from src.mextalki.models.base_model import TimeStampMixin


class UserReferralCredits(TimeStampMixin):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='user_credits',
    )

    credits = models.IntegerField(
        default=0,
    )

    def __str__(self):
        return self.user.email

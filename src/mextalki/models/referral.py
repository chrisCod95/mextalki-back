from django.db import models

from src.mextalki.models.base_model import TimeStampMixin


class Referral(TimeStampMixin):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='referral',
    )
    recommended_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='referrals',
    )
    code = models.CharField(max_length=36, blank=True, null=True)

    purchased_plan = models.BooleanField(default=False)

    earned_credits = models.IntegerField(default=0)

    def __str__(self):
        if self.user:
            return '{id} - {username} - {code}'.format(id=self.id, username=self.user.username, code=self.code)
        return '{id} - {code}'.format(code=self.code, id=self.id)

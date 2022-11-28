from django.db import models
from django.utils.timezone import now

from src.mextalki.models import TimeStampMixin


class Coupon(TimeStampMixin):
    code = models.CharField(
        max_length=255,
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='owners',
        blank=True,
        null=True,
    )
    active = models.BooleanField(
        default=True,
    )
    discount = models.FloatField(default=0)
    times_used = models.IntegerField(default=0)
    times_used_limit = models.IntegerField(default=0)
    is_for_limited_time = models.BooleanField(
        default=False,
        verbose_name='Is for limited time and can be unlimited times used by user',
    )
    limited_time = models.DateField(auto_now=False, auto_now_add=False, default=now)

    def __str__(self):
        if self.owner:
            return '{} by {}'.format(self.code, self.owner)
        return self.code

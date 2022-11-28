from django.db import models

from src.mextalki.models import TimeStampMixin


class UsedCoupon(TimeStampMixin):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='users',
        blank=True,
        null=True,
    )
    coupon = models.ForeignKey(
        'mextalki.Coupon',
        on_delete=models.PROTECT,
        related_name='coupons',
        blank=True,
        null=True,
    )

    def __str__(self):
        return '{} by {}'.format(self.user, self.coupon)

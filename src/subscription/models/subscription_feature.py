from django.db import models

from src.mextalki.models.base_model import TimeStampMixin


class SubscriptionFeature(TimeStampMixin):
    subscription_type = models.ForeignKey(
        'subscription.SubscriptionType',
        on_delete=models.PROTECT,
        related_name='feature',
        null=True,
        blank=True,
        default=None,
    )
    feature = models.CharField(max_length=255)

    def __str__(self):
        return self.feature

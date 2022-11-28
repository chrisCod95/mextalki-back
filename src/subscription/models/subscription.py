import uuid

from django.db import models

from src.mextalki.models.base_model import TimeStampMixin


class Subscription(TimeStampMixin):
    CREATED = 'CREATED'
    ACTIVE = 'ACTIVE'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'

    PAYPAL = 'PAYPAL'
    STRIPE = 'STRIPE'

    STATUS = [
        (CREATED, 'CREATED'),
        (ACTIVE, 'ACTIVE'),
        (CANCELLED, 'CANCELLED'),
        (EXPIRED, 'EXPIRED'),
    ]
    PROVIDERS = [
        (PAYPAL, 'PAYPAL'),
        (STRIPE, 'STRIPE'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='subscriptions',
        blank=True,
        null=True,
    )
    subscription_type = models.ForeignKey(
        'subscription.SubscriptionType',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    active = models.BooleanField(
        default=False,
    )

    status = models.CharField(
        max_length=24,
        choices=STATUS,
        default=CREATED,
    )

    next_billing_time = models.DateTimeField(
        blank=True,
        null=True,
    )
    provider = models.CharField(
        max_length=10,
        choices=PROVIDERS,
    )

    provider_id = models.CharField(max_length=50, blank=True, null=True)

    def cancel(self):
        self.active = False
        self.status = self.CANCELLED
        self.save()

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-created_at',)

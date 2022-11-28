import uuid
from datetime import timedelta

from colorfield.fields import ColorField
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from tinymce import models as tinymce_models

from src.mextalki.models.base_model import TimeStampMixin


class SubscriptionFeature(TimeStampMixin):
    subscription_type = models.ForeignKey(
        'mextalki.SubscriptionType',
        on_delete=models.PROTECT,
        related_name='feature',
        null=True,
        blank=True,
        default=None,
    )
    feature = models.CharField(max_length=255)

    def __str__(self):
        return self.feature


class SubscriptionType(TimeStampMixin):
    USD = 'USD'
    MXN = 'MXN'
    WEEK = 'WEEK'
    MONTH = 'MONTH'
    YEAR = 'YEAR'

    CURRENCIES = [
        (USD, 'USD'),
        (MXN, 'MXN'),
    ]

    BILLING_CYCLE = [
        (WEEK, 'WEEKLY'),
        (MONTH, 'MONTHLY'),
        (YEAR, 'YEARLY'),
    ]

    title = models.CharField(max_length=255)

    price = models.FloatField()
    currency = models.CharField(
        max_length=3,
        choices=CURRENCIES,
        default=USD,
    )
    active = models.BooleanField(
        default=True,
    )
    color = ColorField(default='#FFFFFF')

    billing_cycle = models.CharField(
        max_length=10,
        choices=BILLING_CYCLE,
        default=MONTH,
    )
    paypal_plan_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    stripe_price_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    lesson_time = models.IntegerField(
        default=0,
        help_text='Set in hours',
    )

    practice_time = models.IntegerField(
        default=0,
        help_text='Set in hours',
    )

    extra_hour_lesson_price = models.FloatField(
        default=0,
        help_text='Lesson extra Hour price',
    )
    extra_hour_practice_price = models.FloatField(
        default=0,
        help_text='Practice extra Hour price',
    )
    extra_hour_currency = models.CharField(
        max_length=3,
        choices=CURRENCIES,
        default=USD,
    )
    conversation_club_slots = models.IntegerField(
        default=0,
        help_text='set club access slots',
    )
    has_access_to_courses = models.BooleanField(default=True)
    include_basic_package = models.BooleanField(default=False)
    include_conversation_club = models.BooleanField(default=False)
    include_podcast_features = models.BooleanField(default=False)

    @property
    def uid(self):
        return urlsafe_base64_encode(
            force_bytes(
                '{pk}'.format(pk=self.pk),
            ),
        )

    @property
    def lesson_time_in_minutes(self):
        secs = timedelta(hours=self.lesson_time).total_seconds()
        return int(secs / 60)

    @property
    def practice_time_in_minutes(self):
        secs = timedelta(hours=self.practice_time).total_seconds()
        return int(secs / 60)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('price',)


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
        related_name='old_subscriptions',
        blank=True,
        null=True,
    )
    subscription_type = models.ForeignKey(
        'mextalki.SubscriptionType',
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

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-created_at']

from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from tinymce import models as tinymce_models

from src.mextalki.models.base_model import TimeStampMixin

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class SubscriptionType(TimeStampMixin):
    USD = 'USD'
    MXN = 'MXN'
    MONTH = 'MONTH'
    HALF_YEAR = '6 MONTHS'

    CURRENCIES = [
        (USD, 'USD'),
        (MXN, 'MXN'),
    ]

    BILLING_CYCLE = [
        (MONTH, 'MONTHLY'),
        (HALF_YEAR, '6 MONTHS'),
    ]

    title = models.CharField(max_length=255)

    legacy = models.BooleanField(default=False)

    price = models.FloatField()

    discount = models.FloatField(default=0, validators=PERCENTAGE_VALIDATOR)

    currency = models.CharField(
        max_length=3,
        choices=CURRENCIES,
        default=USD,
    )
    active = models.BooleanField(
        default=True,
    )
    description = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )

    best_deal = models.BooleanField(default=False)

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

    referral_credits = models.IntegerField(
        default=0,
        help_text='earned credits when referral subscribe referrer',
    )

    has_access_to_courses = models.BooleanField(default=True)

    include_basic_package = models.BooleanField(default=True)

    include_conversation_club = models.BooleanField(default=True)

    include_podcast_features = models.BooleanField(default=True)

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

    @property
    def has_discount(self):
        return self.discount > 0

    @property
    def final_price(self):
        price = self.price
        if self.has_discount:
            price = self.price - (self.price * self.discount)
        return price

    def __str__(self):
        if self.legacy:
            return 'LEGACY - {title} / {billing_cycle}'.format(title=self.title, billing_cycle=self.billing_cycle)
        return '{title} / {billing_cycle}'.format(title=self.title, billing_cycle=self.billing_cycle)

    class Meta:
        ordering = ('-billing_cycle', 'price')

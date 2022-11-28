from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from tinymce import models as tinymce_models

from .base_model import TimeStampMixin


class Plan(TimeStampMixin):
    USD = 'USD'
    MXN = 'MXN'

    CURRENCIES = [
        (USD, 'USD'),
        (MXN, 'MXN'),
    ]
    title = models.CharField(max_length=255)
    description = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )
    price = models.FloatField()
    currency = models.CharField(
        max_length=3, choices=CURRENCIES,
        default=USD,
    )
    active = models.BooleanField(
        default=True,
    )
    course = models.ForeignKey(
        'mextalki.Course',
        on_delete=models.PROTECT,
        related_name='plans',
        blank=False,
        null=False,
    )

    @property
    def uid(self):
        return urlsafe_base64_encode(
            force_bytes(
                '{pk}'.format(pk=self.pk),
            ),
        )

    def __str__(self):
        return self.title

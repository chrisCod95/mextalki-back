from django.db import models

from .base_model import TimeStampMixin
from .utils import upload_to_v2


class TeachersReview(TimeStampMixin):
    teacher = models.ForeignKey(
        'mextalki.Teacher',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255)
    review = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    file_path = 'home/testimonials'
    thumbnail = models.ImageField(upload_to=upload_to_v2, default='')

    def __str__(self):
        return '{name} - {subtitle}'.format(name=self.name, subtitle=self.subtitle)

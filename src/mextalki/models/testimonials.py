from django.db import models

from .base_model import TimeStampMixin
from .utils import upload_thumbnail_to


class Testimonial(TimeStampMixin):
    name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    testimonial_video_url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    file_path = 'home/testimonials'
    thumbnail = models.ImageField(upload_to=upload_thumbnail_to, default='')

    def __str__(self):
        return '{name}{subtitle}'.format(name=self.name, subtitle=self.subtitle)

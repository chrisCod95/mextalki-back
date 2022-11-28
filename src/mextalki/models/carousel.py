from django.db import models

from src.mextalki.models.base_model import TimeStampMixin
from src.mextalki.models.utils import upload_image_to


class Carousel(TimeStampMixin):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    button_text = models.CharField(max_length=50, default='')
    button_link = models.CharField(max_length=50, default='')
    file_path = 'home/carousel'
    image = models.ImageField(upload_to=upload_image_to)

    def __str__(self):
        return self.title

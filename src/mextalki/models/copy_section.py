from django.db import models
from tinymce import models as tinymce_models

from src.mextalki.models.base_model import TimeStampMixin
from src.mextalki.models.utils import upload_image_to


class MainCopy(TimeStampMixin):
    title = models.CharField(max_length=255)
    text = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{id} - {title}'.format(id=self.id, title=self.title)

    class Meta:
        verbose_name_plural = 'Your mexican spanish hub - Sections'
        ordering = ('id',)


class HomeCopyInfo(TimeStampMixin):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    text = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )
    icon = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_link = models.CharField(max_length=50, blank=True, null=True)

    image = models.ImageField(upload_to=upload_image_to)
    file_path = 'home/copy_sections'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'What we offer - Sections'

from django.db import models
from sort_order_field import SortOrderField
from tinymce import models as tinymce_models

from .base_model import TimeStampMixin
from .utils import upload_file_to


class UsefulSpanish(TimeStampMixin):
    lesson = models.OneToOneField(
        'mextalki.Lesson',
        on_delete=models.CASCADE,
        related_name='useful_spanish',
    )

    def get_audios(self):
        return self.audio_resources.all()

    class Meta:
        verbose_name_plural = 'Lessons - Useful Spanish'


class UsefulSpanishAudio(TimeStampMixin):
    title = models.CharField(max_length=100)
    description = models.CharField(
        blank=True,
        null=True,
        max_length=100,
    )
    file_path = 'useful_spanish/audios'
    file = models.FileField(upload_to=upload_file_to)
    useful_spanish = models.ForeignKey(
        'mextalki.UsefulSpanish',
        on_delete=models.CASCADE,
        related_name='audio_resources',
    )
    sort_order = SortOrderField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('sort_order',)

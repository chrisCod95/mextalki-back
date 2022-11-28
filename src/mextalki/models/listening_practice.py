from django.db import models
from sort_order_field import SortOrderField
from tinymce import models as tinymce_models

from .base_model import TimeStampMixin
from .utils import upload_file_to


class ListeningPractice(TimeStampMixin):
    description = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )
    lesson = models.OneToOneField(
        'mextalki.Lesson',
        on_delete=models.CASCADE,
        related_name='listening_practice',
    )

    def get_audios(self):
        return self.audio_resources.all()

    def __str__(self):
        return 'Listening practice for - {lesson}'.format(lesson=self.lesson)

    class Meta:
        verbose_name_plural = 'Lessons - Listening Practices'


class ListeningPracticeAudio(TimeStampMixin):
    title = models.CharField(max_length=255)
    transcription = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )
    answer = tinymce_models.HTMLField()
    file_path = 'listening_practices/audios'
    file = models.FileField(upload_to=upload_file_to)
    listening_practice = models.ForeignKey(
        'mextalki.ListeningPractice',
        on_delete=models.CASCADE,
        related_name='audio_resources',
    )
    sort_order = SortOrderField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('sort_order',)

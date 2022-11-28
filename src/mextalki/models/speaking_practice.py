from django.db import models
from sort_order_field import SortOrderField
from tinymce import models as tinymce_models

from .base_model import TimeStampMixin
from .utils import upload_file_to


class SpeakingPractice(TimeStampMixin):
    SPEAKING_PRACTICE = 'Speaking Practice'
    EXERCISES = 'Exercises'

    SECTION_TITLES = [
        (SPEAKING_PRACTICE, 'Speaking Practice'),
        (EXERCISES, 'Exercises'),
    ]
    section_title = models.CharField(
        max_length=50,
        choices=SECTION_TITLES,
        default=SPEAKING_PRACTICE,
    )
    description = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )
    lesson = models.OneToOneField(
        'mextalki.Lesson',
        on_delete=models.CASCADE,
        related_name='speaking_practice',
    )
    bottom_message = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )

    def get_resources(self):
        return self.resources.all()

    def get_audios(self):
        return self.audio_resources.all()

    def __str__(self):
        return 'Speaking practice for - {lesson}'.format(lesson=self.lesson)

    class Meta:
        verbose_name_plural = 'Lessons - Speaking Practices'


class SpeakingPracticeResource(TimeStampMixin):
    url = models.URLField()
    title = models.CharField(max_length=50)
    speaking_practice = models.ForeignKey(
        'mextalki.SpeakingPractice',
        on_delete=models.CASCADE,
        related_name='resources',
    )
    sort_order = SortOrderField()

    def __str__(self):
        return '{url}'.format(url=self.url)


class SpeakingPracticeAudio(TimeStampMixin):
    title = models.CharField(max_length=255)
    description = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )
    file_path = 'speaking_practices/audios'
    file = models.FileField(upload_to=upload_file_to)
    speaking_practice = models.ForeignKey(
        'mextalki.SpeakingPractice',
        on_delete=models.CASCADE,
        related_name='audio_resources',
    )
    sort_order = SortOrderField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('sort_order',)

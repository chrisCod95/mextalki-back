from django.db import models
from django.conf import settings

from tinymce import models as tinymce_models

from src.mextalki.models.utils import upload_to_v2
from src.mextalki.models.base_model import TimeStampMixin


class ImageLessonActivity(TimeStampMixin):
    image = models.ImageField(
        upload_to=upload_to_v2,
        default='',
    )
    file_path = 'lesson_activities/images'
    lesson_activity = models.ForeignKey(
        'mextalki.LessonActivity',
        on_delete=models.CASCADE,
        related_name='images'
    )

    @property
    def image_url(self):
        return 'https://{bucket_name}.s3.amazonaws.com/media/{file_name}'.format(
            bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
            file_name=self.image.name
        )


class LessonActivity(TimeStampMixin):
    activity_description = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )
    lesson = models.OneToOneField(
        'mextalki.Lesson',
        on_delete=models.CASCADE,
        related_name='activity',
    )

    def __str__(self):
        return 'Activity for - {lesson}'.format(lesson=self.lesson)

    class Meta:
        verbose_name_plural = 'Lessons - Activities'

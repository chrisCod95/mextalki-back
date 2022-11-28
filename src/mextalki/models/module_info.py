from django.db import models
from tinymce import models as tinymce_models

from src.mextalki.models.base_model import TimeStampMixin


class ModuleInfo(TimeStampMixin):

    url = models.URLField()

    spanish_transcription = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )
    english_transcription = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )

    lesson = models.OneToOneField(
        'mextalki.Lesson',
        on_delete=models.CASCADE,
        related_name='module_info',
    )

    class Meta:
        verbose_name_plural = 'Modules - Module Info'

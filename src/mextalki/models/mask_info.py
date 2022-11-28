from django.db import models
from tinymce import models as tinymce_models

from src.mextalki.models.base_model import TimeStampMixin
from src.mextalki.models.utils import upload_to_v2


class MaskCopy(TimeStampMixin):
    title = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    how_get_points = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class MaskInfo(TimeStampMixin):
    mask_copy = models.ForeignKey(
        'mextalki.MaskCopy',
        on_delete=models.CASCADE,
        related_name='masks',
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    info = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )
    file_path = 'conversation_club'
    mask_image = models.ImageField(upload_to=upload_to_v2)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

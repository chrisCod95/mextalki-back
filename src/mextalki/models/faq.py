from django.db import models
from tinymce import models as tinymce_models

from src.mextalki.models.base_model import TimeStampMixin


class Faq(TimeStampMixin):
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class FaqQuestion(TimeStampMixin):
    faq = models.ForeignKey(
        'mextalki.Faq',
        on_delete=models.CASCADE,
        related_name='questions',
    )

    question = models.CharField(max_length=255)
    answer = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

from django.db import models
from sort_order_field import SortOrderField

from .base_model import TimeStampMixin


class LessonVideo(TimeStampMixin):
    url = models.URLField()
    lesson = models.ForeignKey(
        'mextalki.Lesson',
        on_delete=models.CASCADE,
        related_name='videos',
    )
    sort_order = SortOrderField()

    def __str__(self):
        return '{url}'.format(url=self.url)

    class Meta:
        ordering = ('sort_order',)

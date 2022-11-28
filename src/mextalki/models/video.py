from django.db import models
from sort_order_field import SortOrderField
from taggit.managers import TaggableManager

from src.mextalki.models.base_model import TimeStampMixin


class Video(TimeStampMixin):

    sort_order = SortOrderField()

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True, null=True)

    thumbnail_url = models.CharField(max_length=255)

    youtube_video_id = models.CharField(max_length=255)

    active = models.BooleanField(
        default=True,
    )

    slug = models.SlugField(blank=False, null=False, default='')

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('sort_order',)

from django.db import models
from sort_order_field import SortOrderField
from taggit.managers import TaggableManager
from tinymce import models as tinymce_models

from src.mextalki.models.base_model import TimeStampMixin
from src.mextalki.models.utils import upload_to_v2


class Podcast(TimeStampMixin):

    sort_order = SortOrderField()

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True, null=True)

    thumbnail_url = models.CharField(max_length=255)

    youtube_video_id = models.CharField(max_length=255)

    blog_content = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )

    transcript = models.FileField(
        upload_to=upload_to_v2,
        default=None,
        blank=True,
        null=True,
    )

    mp3_file = models.FileField(
        upload_to=upload_to_v2,
        default=None,
        blank=True,
        null=True,
    )

    captions = models.FileField(
        upload_to=upload_to_v2,
        default=None,
        blank=True,
        null=True,
    )

    file_path = 'podcasts/transcripts'

    active = models.BooleanField(
        default=True,
    )

    tags = TaggableManager(blank=True)

    slug = models.SlugField(blank=False, null=False, default='')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('sort_order',)

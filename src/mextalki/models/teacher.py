import uuid

from django.conf import settings
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from timezone_field import TimeZoneField
from tinymce import models as tinymce_models

from src.mextalki.models import EventType
from src.mextalki.models.base_model import TimeStampMixin
from src.mextalki.models.utils import upload_image_to


class TeacherToken(TimeStampMixin):
    teacher = models.OneToOneField(
        'mextalki.Teacher',
        on_delete=models.PROTECT,
        related_name='token',
        blank=True,
        null=True,
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return '{teacher} - {uuid}'.format(teacher=self.teacher, uuid=self.uuid)


class Teacher(TimeStampMixin):
    name = models.CharField(max_length=255)
    description = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )
    active = models.BooleanField(
        default=True,
    )
    user = models.OneToOneField(
        'users.User',
        on_delete=models.PROTECT,
        related_name='teacher_profile',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    file_path = 'teachers'
    image = models.ImageField(upload_to=upload_image_to)

    presentation_video = models.URLField(blank=True, null=True)

    time_zone = TimeZoneField(default=settings.TIME_ZONE)

    def lesson_events(self):
        return self.event_types.filter(active=True, type=EventType.LESSON).order_by('title')

    def practice_events(self):
        return self.event_types.filter(active=True, type=EventType.PRACTICE).order_by('title')

    @property
    def uid(self):
        return urlsafe_base64_encode(
            force_bytes(
                '{pk}'.format(pk=self.pk),
            ),
        )

    class Meta:
        ordering = ('name',)

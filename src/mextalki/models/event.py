from datetime import datetime, timedelta, timezone
import uuid

from django.conf import settings
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from timezone_field import TimeZoneField
from tinymce import models as tinymce_models

from src.mextalki.models.base_model import TimeStampMixin


class EventType(TimeStampMixin):
    LESSON = '1'
    PRACTICE = '2'
    CONVERSATION_CLUB = '3'

    EVENT_TYPE = [
        (LESSON, 'LESSON'),
        (PRACTICE, 'PRACTICE'),
        (CONVERSATION_CLUB, 'CONVERSATION_CLUB'),
    ]

    title = models.CharField(max_length=255)

    type = models.CharField(
        max_length=10,
        choices=EVENT_TYPE,
        default=LESSON,
    )

    description = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )

    active = models.BooleanField(
        default=True,
    )

    event_duration = models.IntegerField(
        default=0,
        help_text='Set in minutes',
    )

    teacher = models.ForeignKey(
        'mextalki.Teacher',
        on_delete=models.PROTECT,
        related_name='event_types',
        null=True,
        blank=True,
    )

    calendar_url = models.URLField()

    @property
    def uid(self):
        return urlsafe_base64_encode(
            force_bytes(
                '{pk}'.format(pk=self.pk),
            ),
        )

    def __str__(self):
        if not self.teacher:
            return self.title
        return '{title} with {teacher}'.format(
            title=self.title,
            teacher=self.teacher,
        )

    def is_conversation_club(self):
        return self.type == self.CONVERSATION_CLUB

    def is_practice(self):
        return self.type == self.PRACTICE

    def is_lesson(self):
        return self.type == self.LESSON

    class Meta:
        verbose_name_plural = 'Scheduled events - Types'


class ScheduledEvent(TimeStampMixin):
    ACTIVE = 'ACTIVE'
    CANCELLED = 'CANCELLED'
    RESCHEDULED = 'RESCHEDULED'

    CALENDLY = 'CALENDLY'

    STATUS = [
        (ACTIVE, 'ACTIVE'),
        (CANCELLED, 'CANCELLED'),
        (RESCHEDULED, 'RESCHEDULED'),
    ]
    PROVIDERS = [
        (CALENDLY, 'CALENDLY'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    start_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    time_zone = TimeZoneField(default=settings.TIME_ZONE)

    provider = models.CharField(
        max_length=10,
        choices=PROVIDERS,
        null=True,
        blank=True,
    )
    provider_event_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    provider_invite_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='user_scheduled_events',
    )

    teacher = models.ForeignKey(
        'mextalki.Teacher',
        on_delete=models.PROTECT,
        related_name='teacher_scheduled_events',
        null=True,
        blank=True,
    )

    event_type = models.ForeignKey(
        'mextalki.EventType',
        on_delete=models.PROTECT,
    )
    location = models.URLField(
        default='',
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=24,
        choices=STATUS,
        default=ACTIVE,
    )

    scheduled_with_subscription_time = models.IntegerField(
        default=0,
        help_text='Set in minutes',
    )

    scheduled_with_purchased_time = models.IntegerField(
        default=0,
        help_text='Set in minutes',
    )

    @property
    def user_can_reschedule(self):
        hours_delta = ((self.start_time - datetime.now(timezone.utc)).total_seconds() / 3600)
        if hours_delta > 12:
            return True
        return False

    @property
    def is_rescheduled(self) -> bool:
        return self.status == self.RESCHEDULED

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['-created_at']

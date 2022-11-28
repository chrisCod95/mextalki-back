from django.db import models
from sort_order_field import SortOrderField
from tinymce import models as tinymce_models

from src.mextalki.models.base_model import TimeStampMixin
from src.mextalki.models.utils import upload_to_v2


class ConversationClubInfo(TimeStampMixin):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    club_info = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )
    video_example_url = models.URLField(blank=True, null=True)

    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_link = models.CharField(max_length=50, blank=True, null=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ConversationClubSchedule(TimeStampMixin):
    SUNDAY = '0'
    MONDAY = '1'
    TUESDAY = '2'
    WEDNESDAY = '3'
    THURSDAY = '4'
    FRIDAY = '5'
    SATURDAY = '6'

    WEEK_DAYS = [
        (SUNDAY, 'Sunday'),
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
    ]
    copy = models.ForeignKey(
        'mextalki.ConversationClubInfo',
        on_delete=models.CASCADE,
        related_name='schedules_list',
        null=True,
        blank=True,
        default=None,
    )
    day = models.CharField(
        max_length=255,
        choices=WEEK_DAYS,
        default=SUNDAY,
    )
    hour = models.TimeField(null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)


class ConversationClubTestimonial(TimeStampMixin):
    copy = models.ForeignKey(
        'mextalki.ConversationClubInfo',
        on_delete=models.CASCADE,
        related_name='testimonials_list',
        null=True,
        blank=True,
        default=None,
    )

    language = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    file_path = 'conversation_club'
    thumbnail = models.ImageField(upload_to=upload_to_v2)
    flag_thumbnail = models.ImageField(upload_to=upload_to_v2)
    testimonial_video_url = models.URLField(blank=True, null=True)
    sort_order = SortOrderField()

    def __str__(self):
        return '{id} {language}'.format(id=self.pk, language=self.language)

    class Meta:
        ordering = ('sort_order',)

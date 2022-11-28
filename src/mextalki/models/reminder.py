from django.db import models

from src.mextalki.models.base_model import TimeStampMixin


class Reminder(TimeStampMixin):
    ACTIVE = 'ACTIVE'
    CANCELLED = 'CANCELLED'
    RESCHEDULED = 'RESCHEDULED'

    STATUS_OPTIONS = [
        (ACTIVE, 'ACTIVE'),
        (CANCELLED, 'CANCELLED'),
        (RESCHEDULED, 'RESCHEDULED'),
    ]

    scheduled_event = models.ForeignKey(
        'mextalki.ScheduledEvent',
        on_delete=models.PROTECT,
        related_name='reminders',
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='event_reminders',
        default=None,
    )
    event_status = models.CharField(
        max_length=24,
        choices=STATUS_OPTIONS,
        default=ACTIVE,
    )
    reminder_schedule = models.DateTimeField()
    reminder_was_sent = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Scheduled Events - Reminders'

    def __str__(self):
        return str(self.pk)

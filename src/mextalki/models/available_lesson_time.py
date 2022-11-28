from django.db import models

from .base_model import TimeStampMixin


class UserAvailableLessonTime(TimeStampMixin):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='user_available_lesson_time',
    )

    lesson_time = models.IntegerField(
        default=0,
        help_text='Set in minutes',
    )
    purchased_lesson_time = models.IntegerField(
        default=0,
        help_text='Set in minutes',
    )

    practice_time = models.IntegerField(
        default=0,
        help_text='Set in minutes',
    )
    purchased_practice_time = models.IntegerField(
        default=0,
        help_text='Set in minutes',
    )
    conversation_club_slots = models.IntegerField(
        default=0,
        help_text='set club access slots',
    )
    purchased_conversation_club_slots = models.IntegerField(
        default=0,
        help_text='set club access slots',
    )

    def __str__(self):
        return self.user.email

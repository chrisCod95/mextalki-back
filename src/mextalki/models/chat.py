import uuid
from django.db import models

from src.mextalki.models.base_model import TimeStampMixin


class Chat(TimeStampMixin):
    chat_uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    users = models.ManyToManyField(
        'users.User',
        related_name='chats'
    )
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    unread_messages = models.IntegerField(default=0)

    @property
    def has_reported_messages(self):
        return self.messages.filter(reported=True)

    @property
    def last_message(self):
        return self.messages.filter(reported=False).order_by('-created_at').first()

    def __str__(self):
        return '{uuid} - {updated_at}'.format(uuid=self.chat_uuid, updated_at=self.updated_at)

    class Meta:
        ordering = ('-updated_at', )


class ChatMessage(TimeStampMixin):
    chat = models.ForeignKey(
        'mextalki.Chat',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='messages',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=510)
    is_unread = models.BooleanField(default=True)
    reported = models.BooleanField(default=False)

    def __str__(self):
        return '{owner}: {content}'.format(
            owner=self.user,
            content=self.content,
        )

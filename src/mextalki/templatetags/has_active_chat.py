from django import template

from src.mextalki.models import Chat
from src.users.models import User
from src.mextalki.utils import get_user_by_uid

register = template.Library()


@register.filter(name='has_active_chat')
def has_active_chat(value: str, request_user: User) -> bool:
    user = get_user_by_uid(value)
    try:
        return Chat.objects.filter(users__id=user.pk).get(users__id=request_user.pk)
    except Chat.DoesNotExist:
        return False

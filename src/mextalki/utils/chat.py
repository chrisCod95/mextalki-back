from src.mextalki.models import Chat
from src.users.models import User


def show_unread_messages(chat: Chat, request_user: User) -> bool:
    return chat.last_message.user != request_user


def reset_unread_messages(chat: Chat, request_user: User) -> bool:
    if chat.last_message:
        return chat.last_message.user != request_user
    return False

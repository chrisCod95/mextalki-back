import calendar
from types import MappingProxyType

from django.http import Http404
from django.views.generic import TemplateView
from django.utils import timezone

from src.users.models import User
from src.mextalki.utils import get_user_by_uid, reset_unread_messages
from src.mextalki.models import (
    Challenge,
    LeadershipBoardInfo,
    LeadershipScore,
    Chat, BlogPost, Announcement,
)


class ForumHomeView(TemplateView):
    template_name = 'forum/index.html'
    main_context: str = None
    CONTEXT_OPTIONS = MappingProxyType({
        'blog': 'BLOG',
        'announcements': 'ANNOUNCEMENTS',
        'chat': 'CHAT',
    })

    def get(self, request, *args, **kwargs):
        self.main_context = self.CONTEXT_OPTIONS[kwargs['main_context']]
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers_to_chat'] = self._get_teachers_to_chat()
        context['leaders'] = self._get_leaders(5)
        context['leadership_board_month'] = calendar.month_name[timezone.now().month]
        context['leadership_board_info'] = self._get_board_info()
        context['podium'] = self._get_leaders(3)
        context['main_queryset'] = self._get_main_queryset()
        context['main_context'] = self.main_context
        return context

    def _get_main_queryset(self):
        if self.main_context == self.CONTEXT_OPTIONS['blog']:
            return BlogPost.objects.filter(active=True).order_by('-created_at')

        elif self.main_context == self.CONTEXT_OPTIONS['announcements']:
            return Announcement.objects.filter(active=True).order_by('-created_at')

        elif self.main_context == self.CONTEXT_OPTIONS['chat']:
            return self._get_chats()

        return BlogPost.objects.filter(active=True).order_by('-created_at')

    @staticmethod
    def _get_teachers_to_chat():
        return User.objects.filter(is_teacher=True)

    def _get_chats(self):
        if self.request.user.is_authenticated:
            return Chat.objects.filter(users__id=self.request.user.pk)
        return []

    @staticmethod
    def _get_leaders(limit: int = 3):
        now = timezone.now()
        return LeadershipScore.objects.filter(
            active=True,
            created_at__month=now.month,
            created_at__year=now.year,
        )[:limit]

    @staticmethod
    def _get_board_info():
        try:
            return LeadershipBoardInfo.objects.get(active=True)
        except LeadershipBoardInfo.DoesNotExist:
            return None


class ChatDetailView(TemplateView):
    template_name = 'chat/teacher_room.html'
    chat: Chat = None
    user_to_chat: User = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user_to_chat = self._get_user_to_chat()
        if not self.user_to_chat:
            raise Http404()
        self.chat = self._get_or_create_chat()

    def get(self, request, *args, **kwargs):
        if self.chat.unread_messages and reset_unread_messages(self.chat, self.request.user):
            self.chat.unread_messages = 0
            self.chat.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_chat'] = self.chat
        context['user_to_chat'] = self.user_to_chat
        context['teachers_to_chat'] = self._get_teachers_to_chat()
        context['chats'] = self._get_chats()
        return context

    @staticmethod
    def _get_teachers_to_chat():
        return User.objects.filter(is_teacher=True)

    def _get_chats(self):
        if self.request.user.is_authenticated:
            return Chat.objects.filter(users__id=self.request.user.pk)
        return []

    def _get_user_to_chat(self):
        user_to_chat = get_user_by_uid(self.kwargs['user_uid_b64'])
        if user_to_chat.is_teacher or self.request.user.is_teacher:
            return user_to_chat

    def _get_or_create_chat(self) -> Chat:
        request_user = self.request.user
        chat = Chat.objects.filter(users=self.user_to_chat).filter(users=request_user)
        if not chat:
            chat = Chat()
            chat.save()
            chat.users.add(request_user, self.user_to_chat)
            chat.save()
            return chat
        return chat.first()

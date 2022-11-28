from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from src.mextalki.models import (
    ConversationClubInfo,
    ConversationClubTestimonial,
    EventType,
)
from src.mextalki.utils.get_extra_hour_price import get_extra_hour_price


class NoSeatsConversationClubView(TemplateView):
    template_name = 'conversation_club/without_seats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_type'] = 'Conversation Club'
        context['extra_seat_options'] = [1, 2, 3, 4]
        context['extra_seat_price'] = get_extra_hour_price(
            self.request.user, 'conversation_club',
        )
        context['extra_seat_currency'] = settings.EXTRA_HOUR_CURRENCY
        return context


class ConversationClubView(TemplateView):
    template_name = 'conversation_club/conversation_club.html'
    unauth_user_template_name = 'conversation_club/conversation_club_unauth_user.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not self.user_have_seats():
                return redirect(reverse_lazy('no_seats_conversation_club'))
            return super().get(request, *args, **kwargs)
        return render(
            request=self.request,
            template_name=self.unauth_user_template_name,
            context=self.get_context_data(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conversation_club_info'] = self.get_main_copy()
        context['testimonials'] = Paginator(
            ConversationClubTestimonial.objects.filter(active=True),
            3,
        )
        context['user_available_slots'] = self.available_conversation_club_slots()
        context['event_type'] = self.get_event_type()
        return context

    def get_event_type(self):
        try:
            return EventType.objects.filter(type=EventType.CONVERSATION_CLUB).first()
        except EventType.DoesNotExist:
            return None

    def available_conversation_club_slots(self):
        user = self.request.user
        if user.is_authenticated:
            return user.total_available_conversation_club_slots
        return 0

    def get_main_copy(self):
        return ConversationClubInfo.objects.filter(
            active=True,
        ).first()

    def user_have_seats(self):
        return self.available_conversation_club_slots() > 0

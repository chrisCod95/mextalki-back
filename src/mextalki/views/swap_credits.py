
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import TemplateView

from src.mextalki.utils.get_extra_hour_price import (
    get_extra_hour_info,
    get_extra_hour_price,
)
from src.mextalki.views.constants import BUY_EXTRA_LESSON_EVENT_TYPES


class ExchangeCreditsView(LoginRequiredMixin, TemplateView):
    template_name = 'lessons/exchange_credits.html'

    def get(self, request, *args, **kwargs):
        if kwargs.get('event_type') not in BUY_EXTRA_LESSON_EVENT_TYPES.values():
            raise Http404()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        event_type: str = self.kwargs.get('event_type', '')
        context = super().get_context_data(**kwargs)
        currency, title, color = get_extra_hour_info(self.request.user)
        context['discount'] = self.request.user.referral_credits
        context['event_type'] = self.kwargs.get('event_type')
        context['extra_hour_price'] = get_extra_hour_price(
            self.request.user, event_type,
        )
        context['extra_hour_currency'] = currency
        context['extra_hour_title'] = title
        context['extra_hour_color'] = color
        context['extra_hour_options'] = [1, 2, 3, 4]
        return context


class ExchangeCreditsConvoClubView(LoginRequiredMixin, TemplateView):
    template_name = 'conversation_club/exchange_credits.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currency, title, color = get_extra_hour_info(self.request.user)
        context['discount'] = self.request.user.referral_credits
        context['extra_seat_price'] = get_extra_hour_price(
            self.request.user, 'conversation_club',
        )
        context['extra_seat_currency'] = currency
        context['extra_seat_options'] = [1, 2, 3, 4]
        return context

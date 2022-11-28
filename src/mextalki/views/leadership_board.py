import calendar

from django.utils import timezone
from django.views.generic import TemplateView

from src.mextalki.models import LeaderBoardRewards, LeadershipScore


class LeadershipBoardView(TemplateView):
    template_name = 'leadership_board_view/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leaders'] = self._get_leaders(10)
        context['podium'] = self._get_leaders(3)
        context['leadership_board_month'] = calendar.month_name[timezone.now().month]
        context['leaderboard_rewards'] = LeaderBoardRewards.objects.filter(
            active=True,
        ).first()
        return context

    def _get_leaders(self, limit: int = 3):
        now = timezone.now()
        return LeadershipScore.objects.filter(
            active=True,
            created_at__month=now.month,
            created_at__year=now.year,
        )[:limit]

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from src.subscription.models import SubscriptionType


class NewSubscriptionView(TemplateView):
    template_name = 'subscription/index.html'
    dashboard_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['monthly_subscription_types'] = SubscriptionType.objects.filter(
            active=True,
            billing_cycle=SubscriptionType.MONTH,
        )
        context['biannually_subscription_types'] = SubscriptionType.objects.filter(
            active=True,
            billing_cycle=SubscriptionType.HALF_YEAR,
        )
        return context

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.has_active_subscription:
            return redirect(self.dashboard_url)
        return super().get(request, *args, **kwargs)

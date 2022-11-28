from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class SubscriptionConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'subscription/payment_confirmation.html'

    def get(self, request, *args, **kwargs):
        if not request.user.has_active_subscription:
            return redirect(reverse_lazy('dashboard'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscription'] = self.request.user.last_subscription
        return context

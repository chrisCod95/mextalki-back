from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from src.mextalki.paypal import cancel_subscription as cancel_paypal_subscription
from src.mextalki.stripe import delete_subscription as cancel_stripe_subscription
from src.subscription.forms import CancelSubscriptionForm
from src.subscription.logger import logger
from src.subscription.models import Subscription


class CancelSubscriptionView(LoginRequiredMixin, FormView):
    template_name = 'subscription/cancel.html'
    index_url = reverse_lazy('index')
    form_class = CancelSubscriptionForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        subscription: Subscription = self.request.user.last_subscription
        reason = form.cleaned_data.get('reason')
        try:
            if subscription.provider == Subscription.PAYPAL:
                cancel_paypal_subscription(subscription.provider_id, reason)
            elif subscription.provider == Subscription.STRIPE:
                cancel_stripe_subscription(subscription.provider_id)
            subscription.cancel()
        except Exception as error:
            messages.error(self.request, 'Error trying to cancel your subscription')
            logger.error(error)
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscription']: Subscription = self.request.user.last_subscription
        return context

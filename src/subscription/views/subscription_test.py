from django.views.generic import TemplateView


class SubscriptionTest(TemplateView):
    template_name = 'subscription/test.html'

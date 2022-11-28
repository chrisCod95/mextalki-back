from django.views.generic import TemplateView


class PrivacyPolicy(TemplateView):
    template_name = 'terms_of_use/privacy_policy.html'


class TermsOfUse(TemplateView):
    template_name = 'terms_of_use/terms_of_use.html'


privacy_policy = PrivacyPolicy.as_view()
terms_of_use = TermsOfUse.as_view()

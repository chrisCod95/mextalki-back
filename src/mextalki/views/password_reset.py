from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView

from src.mextalki.logger import logger
from src.users.utils.validate_re_captcha import validate_re_captcha

from src.users.mixins import LogoutRequiredMixin
from .. import forms

INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


class PasswordResetView(LogoutRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'password_reset/password_reset.html'
    reset_password_email = 'password_reset/reset_password_email.html'
    plain_reset_password_email = 'password_reset/plain_reset_password_email.html'
    dashboard_url = reverse_lazy('dashboard')
    form_class = forms.PasswordResetForm
    success_message = 'We send you a recovery password email.'
    success_url = reverse_lazy('password_reset')

    def form_valid(self, form):
        valid_captcha = self._validate_re_captcha()
        if valid_captcha:
            user = self._get_user(form.cleaned_data['email'])
            if user:
                self._send_reset_password_message(user)
                return super().form_valid(form)
            else:
                messages.add_message(
                    self.request, messages.ERROR,
                    'Wrong email please try again',
                )
                return redirect(reverse_lazy('password_reset'))
        messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
        return redirect(reverse_lazy('password_reset'))

    def _send_reset_password_message(self, user):
        current_site = get_current_site(self.request)
        subject = '{site_name} password reset'.format(
            site_name=self.request.site.name,
        )
        context = {
            'site_name': self.request.site.name,
            'user': user,
            'domain': current_site.domain,
            'uid': user.uid,
            'token': self._generate_token(user),
        }
        plain_message = render_to_string(self.plain_reset_password_email, context)
        html_message = render_to_string(self.reset_password_email, context)
        user.email_user(subject, plain_message, html_message=html_message)

    def _get_user(self, email):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(is_active=True, email=email)
        except user_model.DoesNotExist as error:
            logger.error(error)
            user = None
        return user

    def _generate_token(self, user):
        return default_token_generator.make_token(user)

    def _validate_re_captcha(self):
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        return validate_re_captcha(recaptcha_response)


class PasswordResetConfirmView(SuccessMessageMixin, FormView):
    template_name = 'password_reset/password_update.html'
    post_reset_login = False
    reset_url_token = settings.RESET_PASSWORD_TOKEN
    form_class = forms.SetPasswordForm
    success_url = reverse_lazy('dashboard')
    success_message = 'Your account has been updated successfully.'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self._get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if default_token_generator.check_token(self.user, session_token):
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if default_token_generator.check_token(self.user, token):
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token,
                    )
                    return HttpResponseRedirect(redirect_url)
                return redirect(reverse_lazy('index'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        valid_captcha = self._validate_re_captcha()
        if valid_captcha:
            user = form.save()
            del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
            auth_login(self.request, user)
            return super().form_valid(form)
        messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
        return redirect(self.request.path)

    def _get_user(self, uidb64):
        user_model = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = user_model.objects.get(pk=uid)
        except user_model.DoesNotExist as error:
            logger.error(error)
            user = None
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': '',
                'validlink': False,
            })
        return context

    def _validate_re_captcha(self):
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        return validate_re_captcha(recaptcha_response)

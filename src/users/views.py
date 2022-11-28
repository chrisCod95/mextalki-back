import calendar

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView

from src.mextalki.logger import logger
from src.mextalki.models import (
    LeadershipBoardInfo,
    LeadershipScore,
    MaskCopy,
    ScheduledEvent,
)
from src.mextalki.utils import get_user_by_referral_code
from src.users.forms import CustomUserSignUpForm, EditProfileForm, SignInForm
from src.users.mixins import LogoutRequiredMixin
from src.users.utils import (
    create_referral,
    send_verification_message,
    send_welcome_email,
    set_free_lesson_time,
    subscribe_mailchimp_user,
    validate_re_captcha,
    verify_user,
)
from src.users.utils.token import account_activation_token


class SignUpView(LogoutRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'sign_up/sign_up.html'
    form_class = CustomUserSignUpForm
    success_message = 'Your account has been successfully created and activated. Verify your email address to confirm account. If you haven’t received the confirmation email please verify in your spam folder.'  # noqa: E501
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        self._clean_referral_session()
        referral_code = self.request.GET.get('referral_code')
        if referral_code:
            self.request.session.setdefault('referral_code', referral_code)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referral_code = self.request.GET.get('referral_code')
        if referral_code:
            referred_by = get_user_by_referral_code(
                referral_code=referral_code,
            )
            context['referred_by'] = referred_by.username if referred_by else None
        return context

    def form_valid(self, form):
        self._clean_referral_session()
        referral_code = self.request.GET.get('referral_code')
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        valid_captcha = validate_re_captcha(recaptcha_response)
        if valid_captcha:
            user = form.save()
            send_verification_message(user, self.request)
            subscribe_mailchimp_user(user)
            if referral_code:
                create_referral(user, referral_code)
            return super().form_valid(form)
        messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
        return redirect(reverse_lazy('sign_up'))

    def _clean_referral_session(self):
        if 'referral_code' in self.request.session.keys():
            self.request.session.pop('referral_code', None)


class SignInView(LogoutRequiredMixin, FormView):
    template_name = 'login/login.html'
    form_class = SignInForm

    def form_valid(self, form):
        redirect_url = self.request.GET.get('next', reverse_lazy('dashboard'))
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        valid_captcha = validate_re_captcha(recaptcha_response)
        if valid_captcha:
            credentials = form.cleaned_data
            user = authenticate(
                email=credentials['email'], password=credentials['password'],
            )

            if user is not None:
                login(self.request, user)
                return redirect(redirect_url)

            else:
                messages.add_message(
                    self.request, messages.ERROR,
                    'Wrong credentials please try again',
                )
                return redirect(reverse_lazy('login'))
        messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
        return redirect(reverse_lazy('login'))


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scheduled_lessons'] = self.request.user.user_scheduled_events.filter(
            status__in=[ScheduledEvent.ACTIVE, ScheduledEvent.RESCHEDULED],
            end_time__gte=timezone.now(),
        ).order_by('start_time')
        context['masks_copy'] = MaskCopy.objects.filter(active=True).first()
        context['leaders'] = self._get_leaders(5)
        context['leadership_board_month'] = calendar.month_name[timezone.now().month]
        context['leadership_board_place'] = self._get_leadership_board_place()
        context['podium'] = self._get_leaders(3)
        context['leadership_board_info'] = self._get_board_info()
        return context

    def _get_leaders(self, limit: int = 3):
        now = timezone.now()
        return LeadershipScore.objects.filter(
            active=True,
            created_at__month=now.month,
            created_at__year=now.year,
        )[:limit]

    def _get_leadership_board_place(self):
        now = timezone.now()
        leaders_list = list(
            LeadershipScore.objects.filter(
                active=True,
                created_at__month=now.month,
                created_at__year=now.year,
            ).values_list('user', flat=True),
        )
        try:
            return leaders_list.index(self.request.user.id) + 1
        except ValueError:
            return None

    def _get_board_info(self):
        try:
            return LeadershipBoardInfo.objects.get(active=True)
        except LeadershipBoardInfo.DoesNotExist:
            return None


class EditProfileView(SuccessMessageMixin, UpdateView):
    template_name = 'edit_profile/index.html'
    form_class = EditProfileForm
    success_message = 'Your account has been successfully updated.'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('index'))


def verify_view(request, uidb64, token):
    user_model = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk=uid)
    except user_model.DoesNotExist as error:
        logger.error(error)
        user = None
    except(TypeError, ValueError, OverflowError) as error:
        logger.error(error)
        user = None
    valid_token = account_activation_token.check_token(user, token)
    if user is not None and valid_token:
        verify_user(user)
        set_free_lesson_time(user)
        send_welcome_email(user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        message = 'Your account has been verified successfully.'
        messages.success(request, message)
        return redirect(reverse_lazy('subscription'))
    else:
        message = 'Invalid activation link.'
        messages.error(request, message)
        return redirect(reverse_lazy('login'))


def resend_verify_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    send_verification_message(request.user, request)
    return redirect(reverse_lazy('dashboard'))

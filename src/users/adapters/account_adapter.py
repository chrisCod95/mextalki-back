from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse_lazy

from src.users.models import User


def get_existing_user_or_none(user):
    try:
        return User.objects.get(email=user.email)
    except User.DoesNotExist:
        return user


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = get_existing_user_or_none(user)
        return super(AccountAdapter, self).save_user(request, user, form)

    def get_login_redirect_url(self, request):
        return reverse_lazy('dashboard')

    def get_signup_redirect_url(self, request):
        return reverse_lazy('dashboard')

    def get_logout_redirect_url(self, request):
        return reverse_lazy('index')

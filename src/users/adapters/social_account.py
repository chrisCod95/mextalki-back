from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin

from src.users.models import User


def get_existing_user_or_none(user):
    try:
        return User.objects.get(email=user.email)
    except User.DoesNotExist:
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin: SocialLogin, form=None):
        social_login_user = sociallogin.user
        sociallogin.user = (get_existing_user_or_none(social_login_user))
        return super(SocialAccountAdapter, self).save_user(request, sociallogin, form)

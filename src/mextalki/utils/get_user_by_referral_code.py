from typing import Optional

from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

UserModel = get_user_model()


def get_user_by_referral_code(referral_code) -> Optional[UserModel]:
    try:
        username = force_text(urlsafe_base64_decode(referral_code))
        user = UserModel.objects.get(username=username)
    except (ValueError, UserModel.DoesNotExist):
        return None
    return user


def get_user_by_slug(slug) -> Optional[UserModel]:
    try:
        user = UserModel.objects.get(slug=slug)
    except UserModel.DoesNotExist:
        return None
    return user

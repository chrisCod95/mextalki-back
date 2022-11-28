from typing import Optional

from django.contrib.auth import get_user_model

from src.mextalki.models import Referral
from src.mextalki.utils import get_user_by_referral_code

UserModel = get_user_model()

SIGN_UP_REFERRED_CREDITS = 5
SIGN_UP_REFERRAL_CREDITS = 25
MAX_REFERRED_USERS = 100


def create_referral(user: UserModel, referral_code: str) -> Optional[Referral]:
    recommended_by: Optional[UserModel] = get_user_by_referral_code(referral_code)
    if recommended_by:
        if recommended_by.referred_users <= MAX_REFERRED_USERS:
            user.add_referral_credits(SIGN_UP_REFERRAL_CREDITS)
            recommended_by.add_referral_credits(SIGN_UP_REFERRED_CREDITS)
            return Referral(
                code=referral_code,
                user=user,
                recommended_by=recommended_by,
                earned_credits=SIGN_UP_REFERRED_CREDITS,
            ).save()
    return None

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from src.mextalki.logger import logger
from src.mextalki.models import Referral
from src.subscription.models import SubscriptionType

UserModel = get_user_model()


def update_referral_subscription(user: UserModel, subscription_type: SubscriptionType):
    try:
        referral: Referral = user.referral
        if not referral.purchased_plan:
            earned_credits = subscription_type.referral_credits
            referral.earned_credits += earned_credits
            referral.purchased_plan = True
            referral.save()
            recommended_by: UserModel = referral.recommended_by
            recommended_by.add_referral_credits(earned_credits)
    except ObjectDoesNotExist as error:
        logger.error(error)
    except Exception as error:
        logger.error(error)

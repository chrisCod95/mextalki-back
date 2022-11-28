from src.mextalki.models import Coupon, UsedCoupon
from src.mextalki.logger import logger


def set_used_coupon(user, coupon_code: str):
    try:
        coupon = Coupon.objects.get(code=coupon_code)
        coupon.times_used += 1
        coupon.save()
        used_coupon = UsedCoupon(user=user, coupon=coupon)
        used_coupon.save()
    except Coupon.DoesNotExist as error:
        logger.error(error)


def set_used_credits(user, user_credits: str):
    user.remove_referral_credits(int(user_credits))

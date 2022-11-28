from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import FormView

from src.mextalki.forms import CouponForm
from src.mextalki.logger import logger
from src.mextalki.models import Coupon, UsedCoupon
from src.mextalki.utils.get_extra_hour_price import (
    get_extra_hour_info,
    get_extra_hour_price,
)
from src.mextalki.views.constants import BUY_EXTRA_LESSON_EVENT_TYPES


class BuyExtraHoursView(LoginRequiredMixin, FormView):
    template_name = 'lessons/buy_extra_hours.html'
    form_class = CouponForm

    def form_valid(self, form):
        context = self.get_context_data()
        promo_code = form.cleaned_data['promo_code']
        event_type = self.kwargs.get('event_type')
        coupon = self._get_coupon_by_code(promo_code)
        price = get_extra_hour_price(self.request.user, event_type)
        is_valid = self._validate_coupon(coupon)
        coupon_features = self._get_coupon_features(price, coupon, is_valid)

        context.update({
            'extra_hour_price': price,
            **coupon_features,
            'is_valid_coupon': is_valid,
            'show_valid_coupon': True,
            'coupon_code': coupon.code if is_valid else '',
        })
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        if kwargs.get('event_type') not in BUY_EXTRA_LESSON_EVENT_TYPES.values():
            raise Http404()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        event_type: str = self.kwargs.get('event_type', '')
        context = super().get_context_data(**kwargs)
        currency, title, color = get_extra_hour_info(self.request.user)
        price = get_extra_hour_price(self.request.user, event_type)
        context['event_type'] = event_type
        context['extra_hour_price'] = price
        context['extra_hour_currency'] = currency
        context['extra_hour_title'] = title
        context['extra_hour_color'] = color
        context['extra_hour_options'] = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
        context['discount_percentage'] = 0
        context['show_valid_coupon'] = False
        context['is_valid_coupon'] = False
        return context

    def _validate_coupon(self, coupon) -> bool:
        if not coupon:
            return False

        if coupon.is_for_limited_time:
            return date.today() <= coupon.limited_time

        if coupon.times_used >= coupon.times_used_limit:
            return False

        if self.user_used_coupon_times(coupon) > 0:
            return False

        return True

    def _get_coupon_by_code(self, promo_code):
        try:
            return Coupon.objects.get(code=promo_code, active=True)
        except Coupon.DoesNotExist as error:
            logger.error(error)
            return None

    def _get_coupon_features(self, price, coupon, is_valid: bool):
        invalid = {
            'discount_percentage': 0,
            'times_used': 0,
            'times_used_limit': 0,
            'message': 'This coupon is invalid, please try another.',
        }
        if not coupon:
            return invalid

        if not is_valid:
            if coupon.is_for_limited_time and coupon.limited_time <= date.today() or coupon.times_used >= coupon.times_used_limit:  # noqa: E501
                invalid['message'] = 'Oh no this coupon has expired!'
                return invalid
            if self.user_used_coupon_times(coupon) > 0:
                invalid['message'] = "We're sorry but you already used this coupon."
            return invalid

        return {
            'discount_percentage': coupon.discount,
            'times_used': coupon.times_used,
            'times_used_limit': coupon.times_used_limit,
            'message': 'Enjoy your discount',
        }

    def user_used_coupon_times(self, coupon):
        return UsedCoupon.objects.filter(
            user=self.request.user,
            coupon=coupon,
        ).count()

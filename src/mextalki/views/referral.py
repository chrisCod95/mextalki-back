from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.http import Http404
from src.mextalki.utils import get_user_by_slug

UserModel = get_user_model()


@csrf_protect
@require_http_methods(['GET'])
def referral_user_name_view(_, username):
    recommended_by: UserModel = get_user_by_slug(username)
    if recommended_by:
        return redirect(
            get_signup_url(recommended_by.referral_code),
        )
    raise Http404


def get_signup_url(referral_code: str):
    return '{sign_up_url}?referral_code={referral_code}'.format(
        sign_up_url=reverse_lazy('sign_up'),
        referral_code=referral_code,
    )

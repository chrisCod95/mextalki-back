from allauth.account.signals import user_signed_up

from src.users.utils import (
    create_referral,
    send_welcome_email,
    set_free_lesson_time,
    subscribe_mailchimp_user,
    verify_user,
)


def user_signed_up_signal(sender, **kwargs):
    user = kwargs.get('user')
    request = kwargs.get('request')
    referral_code = request.session.pop('referral_code', None)
    if not user.last_login:
        set_free_lesson_time(user)
        verify_user(user)
        subscribe_mailchimp_user(user)
        send_welcome_email(user)
    if referral_code:
        create_referral(user, referral_code)


user_signed_up.connect(receiver=user_signed_up_signal)

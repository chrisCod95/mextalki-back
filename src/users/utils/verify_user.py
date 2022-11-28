from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from src.mextalki.logger import logger
from src.users.utils.token import account_activation_token


def verify_user(user):
    user.verified = True
    user.save()


def set_free_lesson_time(user):
    free_lesson_and_practice_time = settings.FREE_MIN_LESSON_TIME
    user.set_available_lesson_time(free_lesson_and_practice_time)
    user.set_conversation_club_slots(1)


def send_verification_message(user, request):
    current_site = get_current_site(request)
    activation_email = 'sign_up/activation_email.html'
    plain_activation_email = 'sign_up/plain_activation_message.html'

    site_name = request.site.name
    subject = 'Verify {site_name} account'.format(
        site_name=site_name,
    )
    context = {
        'site_name': site_name,
        'user': user,
        'domain': current_site.domain,
        'uid': user.uid,
        'token': _generate_token(user),
    }
    plain_message = render_to_string(plain_activation_email, context)
    html_message = render_to_string(activation_email, context)
    try:
        user.email_user(subject, plain_message, html_message=html_message)
    except Exception as error:
        logger.error(error)


def _generate_token(user):
    return account_activation_token.make_token(user)

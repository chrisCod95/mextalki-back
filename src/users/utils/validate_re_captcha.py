from typing import Optional

import requests
from django.conf import settings


def validate_re_captcha(recaptcha_response: Optional[str]):
    if settings.DEBUG is True:
        return True
    params = {
        'secret': settings.RE_CAPTCHA_SECRET_KEY,
        'response': recaptcha_response,
    }
    response = requests.get(settings.RE_CAPTCHA_URL, params=params, verify=True)
    response_payload = response.json()
    return response_payload.get('success', False)

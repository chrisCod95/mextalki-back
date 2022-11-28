from django.conf import settings
from paypalcheckoutsdk.core import PayPalHttpClient

from src.paypal.logger import logger


class GetSubscriptionRequest:
    def __init__(self, subscription_id):
        self.verb = 'GET'
        self.path = '/v1/billing/subscriptions/{id}'.format(
            id=subscription_id,
        )
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.body = None


class CancelSubscriptionRequest:
    def __init__(self, subscription_id, reason='User cancel subscription'):
        self.verb = 'POST'
        self.path = '/v1/billing/subscriptions/{id}/cancel'.format(
            id=subscription_id,
        )
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.body = {
            'reason': reason,
        }


def get_subscription(subscription_id):
    request = GetSubscriptionRequest(subscription_id=subscription_id)
    client = PayPalHttpClient(settings.PAYPAL_ENVIRONMENT)
    try:
        response = client.execute(request)
        if response.status_code == 200:
            return response.result
    except Exception as error:
        logger.error(error)
    return None


def cancel_subscription(subscription_id, reason):
    request = CancelSubscriptionRequest(subscription_id=subscription_id, reason=reason)
    client = PayPalHttpClient(settings.PAYPAL_ENVIRONMENT)
    response = client.execute(request)
    if response.status_code != 204:
        raise Exception(
            'status code {status_code}'.format(
                status_code=response.status_code,
            ),
        )

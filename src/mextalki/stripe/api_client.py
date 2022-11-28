import stripe
from django.conf import settings


def retrieve_checkout_session(session_id):
    return stripe.checkout.Session.retrieve(
        session_id,
        api_key=settings.STRIPE_SECRET_KEY,
    )


def create_subscription_checkout_session(price_id, success_url, cancel_url):
    return stripe.checkout.Session.create(
        api_key=settings.STRIPE_SECRET_KEY,
        success_url=success_url,
        cancel_url=cancel_url,
        payment_method_types=['card'],
        mode='subscription',
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            },
        ],
    )


def delete_subscription(subscription_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.Subscription.delete(
        subscription_id,
    )


def create_checkout_session(price, product, success_url, cancel_url):
    return stripe.checkout.Session.create(
        api_key=settings.STRIPE_SECRET_KEY,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': price,
                    'product_data': {
                        'name': product,
                    },
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )

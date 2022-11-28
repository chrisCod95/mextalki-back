import logging
from django.forms.models import model_to_dict
from src.mextalki.models import PaypalPayment as OldPaypalPayment
from src.paypal.models import PaypalPayment

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


def run():
    paypal_payments = OldPaypalPayment.objects.all().order_by('-created_at')
    logger.info(OldPaypalPayment.objects.count())

    paypal_payment: OldPaypalPayment
    for paypal_payment in paypal_payments:
        paypal_payment_dict = model_to_dict(paypal_payment)
        new_paypal_payment = PaypalPayment(
            **paypal_payment_dict
        )
        new_paypal_payment.save()
    logger.info(PaypalPayment.objects.count())

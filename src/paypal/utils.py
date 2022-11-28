from src.mextalki.models import Plan
from src.paypal.models import PaypalPayment, PlanPayment


def create_paypal_payment(paypal_payload: dict) -> PaypalPayment:
    paypal_payment = PaypalPayment(
        id=paypal_payload['paypal_id'],
        intent=paypal_payload['paypal_intent'],
        status=paypal_payload['paypal_status'],
        payer_email=paypal_payload['paypal_payer_email'],
        payer_id=paypal_payload['paypal_payer_id'],
        payer_name=paypal_payload['paypal_payer_name'],
        created_at=paypal_payload['paypal_created_at'],
        updated_at=paypal_payload['paypal_updated_at'],
    )
    return paypal_payment.save()


def create_plan_payment(user, plan: Plan, paypal_payment: PaypalPayment) -> PlanPayment:
    plan_payment = PlanPayment(user=user, plan=plan, paypal_payment=paypal_payment)
    return plan_payment.save()

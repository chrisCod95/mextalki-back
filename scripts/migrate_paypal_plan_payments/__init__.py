import logging
from src.mextalki.models import PlanPayment as OldPlanPayment
from src.paypal.models import PlanPayment

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


def run():
    plan_payments = OldPlanPayment.objects.all().order_by('-created_at')
    logger.info(OldPlanPayment.objects.count())
    paypal_payment: OldPlanPayment
    for plan_payment in plan_payments:
        new_plan_payment = PlanPayment(
            id=plan_payment.id,
            user=plan_payment.user,
            plan=plan_payment.plan,
            updated_at=plan_payment.updated_at,
        )
        logger.info(new_plan_payment)
        new_plan_payment.save()
        new_plan_payment.created_at = plan_payment.created_at
        new_plan_payment.updated_at = plan_payment.updated_at
        new_plan_payment.save()
    logger.info(PlanPayment.objects.count())

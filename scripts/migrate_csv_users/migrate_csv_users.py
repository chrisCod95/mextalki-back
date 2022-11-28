import logging
import csv
from pathlib import Path
from django.contrib.auth import get_user_model
from src.mextalki.models import SubscriptionType, Subscription, PlanPayment, Plan
from src.subscription.utils import (
    create_subscription,
)
logger = logging.getLogger('migrate_csv_users')

User = get_user_model()

TEMPORAL_PASSWORD = 'temporal'


def run():
    users: list = _read_csv_file()
    users_with_subscription = 0
    users_with_basic_course = 0
    users_with_intermediate_course = 0

    for user in users:
        email = user.get('email')
        user_name = user.get('username')
        has_subscription = has_value(user['has_subscription'])
        has_basic_course = has_value(user['basic_course'])
        has_intermediate_course = has_value(user['intermediate_course'])
        subscription_type = user.get('subscription_type', None)
        subscription_id = user.get('subscription_id', None)
        if has_subscription:
            users_with_subscription += 1
            provider = _get_provider(subscription_id)
            logger.info('subscription_id: {subscription_id}'.format(subscription_id=subscription_id))
            logger.info('subscription_type: {subscription_type}'.format(subscription_type=subscription_type))
            logger.info('provider: {provider}'.format(provider=provider))
            user = create_user(user_name, email)
            if user:
                _create_subscription(user, subscription_type, provider, subscription_id)
                log_user_info(
                    email,
                    user_name,
                    has_subscription,
                    subscription_type,
                    has_basic_course,
                    has_intermediate_course,
                )
        if has_basic_course or has_intermediate_course and not has_subscription:
            user = create_user(user_name, email)
            if has_basic_course:
                users_with_basic_course += 1
                if user:
                    _create_basic_course(user)
                    log_user_info(
                        email,
                        user_name,
                        has_subscription,
                        subscription_type,
                        has_basic_course,
                        has_intermediate_course,
                    )
            if has_intermediate_course:
                users_with_intermediate_course += 1
                if user:
                    _create_intermediate_course(user)
                    log_user_info(
                        email,
                        user_name,
                        has_subscription,
                        subscription_type,
                        has_basic_course,
                        has_intermediate_course,
                    )
        else:
            user = create_user(user_name, email)
            log_user_info(
                email,
                user_name,
                has_subscription,
                subscription_type,
                has_basic_course,
                has_intermediate_course,
            )
            print('\n')
    logger.info(
        'users with_subscription: {users_with_subscription}'.format(
            users_with_subscription=users_with_subscription,
        )
    )
    logger.info(
        'users with_basic_course: {users_with_basic_course}'.format(
            users_with_basic_course=users_with_basic_course,
        )
    )
    logger.info(
        'users with_intermediate_course: {users_with_intermediate_course}'.format(
            users_with_intermediate_course=users_with_intermediate_course,
        )
    )


def log_user_info(
    email,
    user_name,
    has_subscription,
    subscription_type,
    has_basic_course,
    has_intermediate_course,
):
    logger.info('email: {email}'.format(email=email))
    logger.info('user_name: {user_name}'.format(user_name=user_name))
    logger.info(
        'has_subscription: {has_subscription}'.format(
            has_subscription=has_subscription,
        )
    )
    if has_subscription:
        logger.info(
            'subscription_type: {subscription_type}'.format(
                subscription_type=subscription_type,
            )
        )
    logger.info(
        'has_basic_course: {has_basic_course}'.format(
            has_basic_course=has_basic_course,
        )
    )
    logger.info(
        'has_intermediate_course: {has_intermediate_course}'.format(
            has_intermediate_course=has_intermediate_course,
        )
    )


def create_user(username, email):
    if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
        user = User.objects.create_user(
            username=username,
            email=email,
            password=TEMPORAL_PASSWORD,
            is_active=False,
        )
        user.save()
        return user
    return None


def has_value(value_str: str) -> bool:
    return value_str == 'yes'


def _create_subscription(user, subscription_type_str, provider, provider_id):
    subscription_type = _get_subscription_type(subscription_type_str)
    if subscription_type:
        return create_subscription(user, subscription_type, provider, provider_id)
    return None


def _get_subscription_type(subscription_type):
    try:
        return SubscriptionType.objects.get(title=subscription_type)
    except SubscriptionType.DoesNotExist as error:
        logger.error(error)
        return None


def _get_provider(provider_str: str):
    if provider_str:
        if provider_str.startswith('I-'):
            return Subscription.PAYPAL
        return Subscription.STRIPE
    return None


def _read_csv_file():
    path = _get_path()
    logger.info(path)
    field_names = [
        'username',
        'id',
        'email',
        'password',
        'dont_known',
        'basic_course',
        'intermediate_course',
        'has_subscription',
        'subscription_type',
        'due_date',
        'subscription_id',
        'cancel'
    ]
    with open(f'{path}/users.csv') as file:
        rows = csv.DictReader(file, field_names)
        return [dict(row) for row in rows]


def _get_path():
    return Path(__file__).resolve().parent


def _create_basic_course(user):
    plan = Plan.objects.get(pk=1)
    plan_payment = _create_plan_payment(user, plan)
    return plan_payment


def _create_intermediate_course(user):
    plan = Plan.objects.get(pk=4)
    plan_payment = _create_plan_payment(user, plan)
    return plan_payment


def _create_plan_payment(user, plan):
    plan_payment = PlanPayment(user=user, plan=plan)
    plan_payment.save()
    return plan_payment

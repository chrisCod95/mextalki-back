from django.db import models


class StripePayment(models.Model):
    DRAFT = 'draft'
    OPEN = 'open'
    PAID = 'paid'
    UNCOLLECTIBLE = 'uncollectible'
    VOID = 'void'
    SUBSCRIPTION_CYCLE = 'subscription_cycle'
    SUBSCRIPTION_CREATE = 'subscription_create'
    SUBSCRIPTION_UPDATE = 'subscription_update'
    SUBSCRIPTION = 'subscription'
    MANUAL = 'manual'
    USD = 'USD'
    MXN = 'MXN'
    WEEK = 'WEEK'
    MONTH = 'MONTH'
    YEAR = 'YEAR'

    CURRENCIES = [
        (USD, 'USD'),
        (MXN, 'MXN'),
    ]

    STATUS = [
        (DRAFT, 'draft'),
        (OPEN, 'open'),
        (PAID, 'paid'),
        (UNCOLLECTIBLE, 'uncollectible'),
        (VOID, 'void'),
    ]
    BILLING_REASONS = [
        (SUBSCRIPTION_CYCLE, 'subscription cycle'),
        (SUBSCRIPTION_CREATE, 'subscription create'),
        (SUBSCRIPTION_UPDATE, 'subscription update'),
        (SUBSCRIPTION, 'subscription'),
        (MANUAL, 'manual'),
    ]

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    id = models.CharField(max_length=50, primary_key=True)
    customer_id = models.CharField(max_length=50)
    charge_id = models.CharField(max_length=50)
    subscription_id = models.CharField(max_length=50, blank=True, null=True)
    billing_reason = models.CharField(
        max_length=50,
        choices=BILLING_REASONS,
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCIES,
    )

    customer_email = models.EmailField(blank=True, null=True)
    customer_name = models.CharField(max_length=50, blank=True, null=True)
    customer_phone = models.CharField(max_length=50, blank=True, null=True)
    invoice_pdf = models.CharField(max_length=255, blank=True, null=True)
    payment_intent = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):
        return self.id

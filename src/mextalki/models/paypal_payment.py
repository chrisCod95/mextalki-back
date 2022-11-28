from django.db import models


class PaypalPayment(models.Model):
    INTENT_CHOICES = [
        ('CAPTURE', 'CAPTURE'),
        ('AUTHORIZE', 'AUTHORIZE'),
    ]
    STATUS_CHOICES = [
        ('CREATED', 'CREATED'),
        ('SAVED', 'SAVED'),
        ('APPROVED', 'APPROVED'),
        ('VOIDED', 'VOIDED'),
        ('COMPLETED', 'COMPLETED'),
        ('PAYER_ACTION_REQUIRED', 'PAYER_ACTION_REQUIRED'),
    ]
    id = models.CharField(max_length=20, primary_key=True)
    intent = models.CharField(choices=INTENT_CHOICES, max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    payer_email = models.EmailField()
    payer_id = models.CharField(max_length=20)
    payer_name = models.CharField(max_length=300)

    def __str__(self):
        return self.id

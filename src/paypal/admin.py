from django.contrib import admin

from src.paypal.models import PaypalPayment, PlanPayment


class PlanPaymentAdmin(admin.ModelAdmin):
    model = PlanPayment
    list_display = ('id', 'user', 'plan', 'paypal_payment', 'created_at', 'updated_at')
    list_filter = ('plan',)
    list_display_links = ('id', 'user', 'plan', 'paypal_payment')


class PaypalPaymentAdmin(admin.ModelAdmin):
    model = PaypalPayment
    list_display = (
        'id', 'intent', 'status',
        'payer_email', 'created_at', 'updated_at',
    )
    list_filter = ('status', 'intent')
    list_display_links = ('id',)
    ordering = ('-created_at',)


admin.site.register(PaypalPayment, PaypalPaymentAdmin)
admin.site.register(PlanPayment, PlanPaymentAdmin)

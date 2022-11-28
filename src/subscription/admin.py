from django.contrib import admin
from django.forms import model_to_dict
from src.subscription.models import Subscription, SubscriptionFeature, SubscriptionType


class CustomSubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    list_display = (
        'id',
        'user',
        'active',
        'status',
        'provider',
        'provider_id',
        'next_billing_time',
        'subscription_type',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'subscription_type',
        'active',
        'status',
        'provider',
    )
    search_fields = ('id', 'provider_id', 'user__email')
    list_display_links = ('id', 'user', 'subscription_type')


class CustomSubscriptionFeatureItemAdmin(admin.TabularInline):
    model = SubscriptionFeature
    extra = 0


@admin.action(description='Clone selected rows')
def clone(modeladmin, request, queryset):
    for subscription_type in queryset:
        kwargs = model_to_dict(subscription_type, exclude=['id'])
        new_instance = SubscriptionType.objects.create(**kwargs)
        new_instance.save()


class CustomSubscriptionTypeAdmin(admin.ModelAdmin):
    model = SubscriptionType
    actions = (clone,)
    list_display = (
        'title',
        'price',
        'discount',
        'currency',
        'billing_cycle',
        'active',
        'paypal_plan_id',
        'stripe_price_id',
        'lesson_time',
        'practice_time',
        'extra_hour_lesson_price',
        'extra_hour_practice_price',
        'conversation_club_slots',
        'referral_credits',
        'legacy',
        'created_at',
        'updated_at',
    )
    list_display_links = ('title',)
    search_fields = ('title',)
    list_filter = ('billing_cycle', 'active', 'legacy',)
    inlines = (CustomSubscriptionFeatureItemAdmin,)



admin.site.register(Subscription, CustomSubscriptionAdmin)
admin.site.register(SubscriptionType, CustomSubscriptionTypeAdmin)

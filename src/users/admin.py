import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from src.mextalki.models import (
    UserAvailableLessonTime,
    UserExperiencePoint,
    UserReferralCredits,
)

from .forms import CustomUserChangeForm, CustomUserCreationForm  # noqa: WPS300
from .models import User  # noqa: WPS300


class AvailableLessonTimeInline(admin.TabularInline):
    model = UserAvailableLessonTime
    min_num = 1
    max_num = 1
    can_delete = False


class UserExperiencePointInline(admin.TabularInline):
    model = UserExperiencePoint
    min_num = 1
    max_num = 1
    can_delete = False


class UserReferralCreditsInline(admin.TabularInline):
    model = UserReferralCredits
    min_num = 1
    max_num = 1
    can_delete = False


def export_as_csv(self, request, queryset):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    writer.writerow(['id', 'first_name', 'last_name', 'username', 'email', 'date_joined', 'last_login', 'is_active',
                     'location', 'total_lesson_time', 'total_available_conversation_club_slots', 'total_practice_time',
                     'verified', 'birth_day', 'has_active_subscription'])
    for user in queryset:
        writer.writerow([user.id, user.first_name, user.last_name, user.username, user.email, user.date_joined,
                         user.last_login, user.is_active, user.location, user.total_lesson_time,
                         user.total_available_conversation_club_slots, user.total_practice_time, user.verified,
                         user.birth_day, user.has_active_subscription])

    return response


export_as_csv.short_description = "Export Selected As CSV"


class CustomUserAdmin(UserAdmin):
    readonly_fields = ['referral_code', 'slug', 'has_active_subscription_for_admin',
                       'total_lesson_time', 'total_available_conversation_club_slots', 'total_practice_time']
    fieldsets = (
        (
            None,
            {'fields': ('email', 'password')},
        ),
        (
            _('Personal info'),
            {
                'fields': (
                    'first_name', 'last_name', 'username',
                    'profile_picture', 'referral_code',
                ),
            },
        ),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'verified', 'is_staff', 'is_teacher', 'groups', 'user_permissions'),
            },
        ),
        (
            _('Extra info'),
            {'fields': ('bio', 'location', 'birth_day')},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'username',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                ),
            },
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'has_active_subscription_for_admin', 'username', 'slug',
                    'total_lesson_time', 'total_available_conversation_club_slots', 'total_practice_time')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email', 'username')
    inlines = (
        AvailableLessonTimeInline,
        UserExperiencePointInline, UserReferralCreditsInline,
    )
    actions = [export_as_csv]


admin.site.register(User, CustomUserAdmin)

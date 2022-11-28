from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from src.mextalki.models import Announcement, Course, ScheduledEvent


def seo(request):
    current_site = request.site
    return {
        'seo_site_name': current_site.name,
        'seo_title_prefix': '{site_name} · '.format(site_name=current_site.name),
        'seo_description': settings.SEO_DESCRIPTION,
        'seo_base_url': 'https://{site_domain}'.format(site_domain=request.site.domain),
    }


def recaptcha(request):
    return {
        're_captcha_site_key': settings.RE_CAPTCHA_SITE_KEY,
    }


def courses(requests):
    return {
        'courses': Course.get_active_courses(),
    }


def announcements(requests):
    return {
        'announcements': Announcement.objects.filter(active=True),
    }


def reminders(request):
    start_time = timezone.now()
    end_time = start_time + timedelta(minutes=60)
    if not request.user.is_authenticated:
        return {'reminders': []}
    return {
        'reminders': ScheduledEvent.objects.filter(
            user=request.user,
            start_time__range=(start_time, end_time)
        )
    }


def paypal(request):
    return {
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
    }


def stripe(request):
    return {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }


def google_tag_manager(request):
    return {
        'google_tag_id': settings.GOOGLE_TAG_ID,
        'google_site_tag_analytics_id': settings.GOOGLE_SITE_TAG_ANALYTICS_ID,
        'google_site_tag_ads_id': settings.GOOGLE_SITE_TAG_ADS_ID,
    }


def whatsapp(request):
    return {
        'whatsapp_phone_number': settings.WHATSAPP_PHONE_NUMBER,
    }


def version(request):
    return {
        'version': settings.VERSION,
    }

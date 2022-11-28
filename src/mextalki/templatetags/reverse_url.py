import logging

from django import template
from django.shortcuts import reverse
from django.urls import NoReverseMatch

register = template.Library()
logger = logging.getLogger('django')


@register.filter(name='reverse_url')
def reverse_url(value):
    if not value:
        return ''
    try:
        if value.startswith('#'):
            return value
        return reverse(value)
    except NoReverseMatch as error:
        logger.error(error)
        return reverse('index')

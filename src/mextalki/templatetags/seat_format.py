from django import template

register = template.Library()


@register.filter('seat_format')
def seat_format(value):
    if value is None:
        return ''
    if value > 1:
        return '{value} Seats'.format(value=value)
    return '{value} Seat'.format(value=value)

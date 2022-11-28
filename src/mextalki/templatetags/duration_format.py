from django import template

register = template.Library()


@register.filter('duration_format')
def duration_format(value):
    if value is None:
        return ''
    hour_label = 'hour'
    minute_label = 'min.'
    if isinstance(value, float):
        value = int(value)
    hours = int(value / 60)
    minutes = value % 60
    if hours != 1:
        hour_label += 's'
    if minutes == 0:
        return '{hours} {hour_label}'.format(
            hours=hours,
            hour_label=hour_label,
        )
    return '{hours} {hour_label} - {minutes} {minute_label}'.format(
        hours=hours,
        hour_label=hour_label,
        minutes=minutes,
        minute_label=minute_label,
    )

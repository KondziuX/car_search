from django.utils import timezone
from django import template

register = template.Library()

@register.filter
def custom_timesince(value):
    now = timezone.now()
    diff = now - value

    if diff.days > 0:
        return f"{diff.days} dni temu"
    elif diff.seconds // 3600 > 0:
        hours = diff.seconds // 3600
        return f"{hours} godzin temu"
    elif diff.seconds // 60 > 0:
        minutes = diff.seconds // 60
        return f"{minutes} minut temu"
    else:
        return "przed chwilą"

from django.utils import timezone
from django import template
import locale

locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')

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

@register.filter
def currency(value):
    try:
        value = int(float(value))  # Konwertuje na liczbę całkowitą
    except (TypeError, ValueError):
        return value
    return f"{value:,} PLN".replace(",", " ")

#Pętla dla zdjęć
@register.filter
def subtract(value, arg):
    return value - arg

# booking/templatetags/math_extras.py
from django import template

register = template.Library()

@register.filter
def abs_val(value):
    try:
        return abs(value)
    except Exception:
        return value

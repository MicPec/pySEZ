from django import template
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag
def urlparams(*args, **kwargs):
    if safe_args := {k: v for k, v in kwargs.items() if v is not None}:
        return f"?{urlencode(safe_args)}"
    return ""

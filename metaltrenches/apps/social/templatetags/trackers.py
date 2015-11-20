from django import template
from django.conf import settings
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def ga():
    if settings.DEBUG is False:
        return render_to_string('social/ga.html', {})
    return ''

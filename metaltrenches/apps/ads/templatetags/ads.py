from django import template
from django.conf import settings
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag
def ga():
    if settings.DEBUG is False:
        return render_to_string("ads/ga.html", {})
    return ""


@register.simple_tag
def ad_space():
    if settings.DEBUG is False:
        return render_to_string("ads/advertisement.html", {})
    return render_to_string("ads/placeholder.html", {})

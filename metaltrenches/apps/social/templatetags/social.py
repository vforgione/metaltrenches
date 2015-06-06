from django import template
from django.conf import settings
from django.template.loader import render_to_string


register = template.Library()

@register.simple_tag
def fb_sdk():
    return render_to_string("social/fb-sdk.html", {"app_id": settings.FB_APP_ID})

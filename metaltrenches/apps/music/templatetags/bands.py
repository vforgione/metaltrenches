from django import template
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag
def band_links(band):
    return render_to_string("music/fragments/band-links.html", {"band": band})

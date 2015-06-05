from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.template.defaultfilters import striptags


register = template.Library()


@register.simple_tag
def open_graph(review):
    title = review.title
    if review.subtitle:
        title += ": " + review.subtitle
    context = {
        "title": title,
        "image": "{}{}".format(settings.MEDIA_URL, review.album.cover_art),
        "url": review.get_absolute_url(),
        "description": striptags(review.body[:151]) + " ..."
    }
    return render_to_string("social/open-graph.html", context)


@register.simple_tag
def twitter_card(review):
    title = review.title
    if review.subtitle:
        title += ": " + review.subtitle
    context = {
        "title": title,
        "image": "{}{}".format(settings.MEDIA_URL, review.album.cover_art),
        "url": review.get_absolute_url(),
        "description": striptags(review.body[:151]) + " ..."
    }
    return render_to_string("social/twitter-card.html", context)

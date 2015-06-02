from django import template
from django.template.loader import render_to_string
from django.utils.text import mark_safe


register = template.Library()


@register.simple_tag
def hc_script(album):
    try:
        ratings = [rating for rating in album.ratings.all()]
        sum_scores = sum([r.score for r in ratings])
        len_ratings = len(ratings)
        avg_score = round(sum_scores / len_ratings)
        categories = "["
        scores = "["
        for rating in ratings:
            categories += "'{name}', ".format(name=rating.factor.name)
            scores += "{score}, ".format(score=rating.score)
        categories = categories[:-2] + "]"
        scores = scores[:-2] + "]"
        context = {
            "avg_score": avg_score,
            "categories": mark_safe(categories),
            "album_title": album.title,
            "scores": scores,
        }
        return render_to_string("reviews/partials/charts/hc-script.html", context)

    except Exception as e:
        return ""

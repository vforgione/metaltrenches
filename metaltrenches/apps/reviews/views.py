from annoying.decorators import render_to
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from .models import Review


@cache_page(settings.CACHE_DURATION)
@render_to("reviews/home.html")
def home(request):
    reviews = Review.published_objects.all().order_by("-published")[:13]
    return {
        "reviews": reviews,
    }


@cache_page(settings.CACHE_DURATION)
@render_to("reviews/review-detail.html")
def review_detail(request, slug, pk):
    review = get_object_or_404(Review, pk=pk)
    return {
        "review": review,
    }


@cache_page(settings.CACHE_DURATION)
@render_to("reviews/review-list.html")
def review_list(request):
    reviews = Review.published_objects.all().order_by("-published")
    paginator = Paginator(reviews, 20)
    page = request.GET.get("page")
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    return {
        "reviews": reviews,
    }

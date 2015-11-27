from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from .models import BaseContent, Review, Post, List, Genre, Band, Album, Event


@cache_page(settings.CACHE_DURATION)
def review_detail(request, slug, pk):
    try:
        review = Review.published_objects.get(slug=slug, pk=pk)
        return render_to_response('content/review-detail.html', {'review': review}, RequestContext(request))
    except Review.DoesNotExist:
        list = get_object_or_404(List.objects.all(), slug=slug, pk=pk)
        if list.is_ordered:
            if list.is_ordered_descending:
                items = list.items.all().order_by('-sequence')
            else:
                items = list.items.all().order_by('sequence')
        else:
            items = list.items.all()
        return render_to_response('content/list-detail.html', {'list': list, 'items': items}, RequestContext(request))

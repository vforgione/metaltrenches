from annoying.decorators import render_to
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from .models import Band, Album
from ..reviews.models import Review


@cache_page(settings.CACHE_DURATION)
@render_to("music/band-detail.html")
def band_detail(request, slug):
    band = get_object_or_404(Band.objects.prefetch_related(), slug=slug)
    return {
        "band": band,
    }


@cache_page(settings.CACHE_DURATION)
@render_to("music/band-list.html")
def band_list(request):
    reviews = Review.published_objects.all().prefetch_related()
    hits = set()
    bands = sorted(
        [r.album.band for r in reviews if r.album.band not in hits and not hits.add(r.album.band)],
        key=lambda b: b.name
    )
    paginator = Paginator(bands, 20)
    page = request.GET.get("page")
    try:
        bands = paginator.page(page)
    except PageNotAnInteger:
        bands = paginator.page(1)
    except EmptyPage:
        bands = paginator.page(paginator.num_pages)
    _bands = [b for b in bands]
    if len(_bands):
        first, last = _bands[0], bands[-1]
    else:
        first, last = "", ""
    return {
        "bands": bands,
        "first": first,
        "last": last,
    }


@cache_page(settings.CACHE_DURATION)
@render_to("music/album-detail.html")
def album_detail(request, slug):
    album = get_object_or_404(Album.objects.prefetch_related(), slug=slug)
    return {
        "album": album,
    }


@cache_page(settings.CACHE_DURATION)
@render_to("music/album-list.html")
def album_list(request):
    reviews = Review.published_objects.all().prefetch_related()
    hits = set()
    albums = sorted(
        [r.album for r in reviews if r.album not in hits and not hits.add(r.album)],
        key=lambda a: a.title
    )
    paginator = Paginator(albums, 20)
    page = request.GET.get("page")
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
    _albums = [a for a in albums]
    if len(_albums):
        first, last = _albums[0], _albums[-1]
    else:
        first, last = "", ""
    return {
        "albums": albums,
        "first": first,
        "last": last,
    }

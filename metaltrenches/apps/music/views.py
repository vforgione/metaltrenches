from annoying.decorators import render_to
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from ...utils.iterators import grouper
from .models import Genre, Band, Album, Event


@cache_page(settings.CACHE_DURATION)
@render_to('music/genre-list.html')
def genre_list(request):
    _genres = sorted(Genre.get_published_genres(), key=lambda g: g.name)
    genres = grouper(_genres, 2)
    return {
        'genres': genres,
    }


@cache_page(settings.CACHE_DURATION)
@render_to('music/band-list.html')
def band_list(request):
    _bands = sorted(Band.get_published_bands(), key=lambda b: b.name)
    bands = grouper(_bands, 3)
    return {
        'bands': bands,
    }


@cache_page(settings.CACHE_DURATION)
@render_to('music/album-list.html')
def album_list(request):
    _albums = sorted(Album.get_published_albums(), key=lambda a: a.title)
    albums = grouper(_albums, 3)
    return {
        'albums': albums,
    }


@cache_page(settings.CACHE_DURATION)
@render_to('music/event-list.html')
def event_list(request):
    events = sorted(Event.get_published_events(), key=lambda e: e.name)
    return {
        'events': events,
    }


@cache_page(settings.CACHE_DURATION)
@render_to('music/band-detail.html')
def band_detail(request, slug, pk):
    band = get_object_or_404(Band, slug=slug, pk=pk)
    return {
        'band': band,
    }


@cache_page(settings.CACHE_DURATION)
@render_to('music/album-detail.html')
def album_detail(request, slug, pk):
    album = get_object_or_404(Album, slug=slug, pk=pk)
    return {
        'album': album,
    }

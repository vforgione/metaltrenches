from annoying.decorators import render_to
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from .models import Genre, Band, Album, Event


@cache_page(settings.CACHE_DURATION)
@render_to('music/genre-list.html')
def genre_list(request):
    genres = Genre.objects.all().order_by('name')
    return {
        'genres': genres,
    }


@cache_page(settings.CACHE_DURATION)
@render_to('music/band-list.html')
def band_list(request):
    bands = Band.objects.all().order_by('name')
    return {
        'bands': bands,
    }


@cache_page(settings.CACHE_DURATION)
@render_to('music/album-list.html')
def album_list(request):
    albums = Album.objects.all().order_by('title')
    return {
        'albums': albums,
    }


@cache_page(settings.CACHE_DURATION)
@render_to('music/event-list.html')
def event_list(request):
    events = Event.objects.all().order_by('name')
    return {
        'events': events,
    }

from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from ...utils.iterators import grouper
from .models import BaseContent, Review, Post, List, Genre, Band, Album, Event


@login_required
def preview(request, slug, pk):
    try:
        content = Review.objects.get(slug=slug, pk=pk)
        co = None
        if content.subject.ratings.count():
            co = content.subject
        return render_to_response(
            'content/review-detail.html', {'review': content, 'chart_object': co}, RequestContext(request))

    except Review.DoesNotExist:
        try:
            content = Post.objects.get(slug=slug, pk=pk)
            return render_to_response('content/post-detail.html', {'post': content}, RequestContext(request))

        except Post.DoesNotExist:
            content = get_object_or_404(List, slug=slug, pk=pk)
            if content.is_ordered:
                if content.is_ordered_descending:
                    items = content.items.all().order_by('-sequence')
                else:
                    items = content.items.all().order_by('sequence')
            else:
                items = content.items.all()
            return render_to_response(
                'content/list-detail.html', {'list': content, 'items': items}, RequestContext(request))


@cache_page(settings.CACHE_DURATION)
@render_to('content/home.html')
def home(request):
    # pinned content
    _reviews = Review.published_objects.all().order_by('-published')[:4]
    _lists = List.published_objects.all().order_by('-published')[:4]

    pinned_content = sorted([c for c in _reviews] + [c for c in _lists], key=lambda c: c.published, reverse=True)

    excluded_reviews = [content.pk for content in pinned_content if isinstance(content, Review)] or None
    excluded_lists = [content.pk for content in pinned_content if isinstance(content, List)] or None
    exclusion_mapping = {
        Review: excluded_reviews,
        Post: Post.published_objects.all().values_list('pk', flat=True),
        List: excluded_lists,
    }

    # list of content
    content = BaseContent.get_all_published(limit=15, exclusion_mapping=exclusion_mapping)

    # posts
    posts = Post.published_objects.all()

    return {
        'pinned_content': pinned_content,
        'content': content,
        'posts': posts,
    }


@cache_page(settings.CACHE_DURATION)
def review_detail(request, slug, pk):
    try:
        review = Review.published_objects.get(slug=slug, pk=pk)
        co = None
        if review.subject.ratings.count():
            co = review.subject
        return render_to_response('content/review-detail.html', {'review': review, 'chart_object': co}, RequestContext(request))
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


@cache_page(settings.CACHE_DURATION)
@render_to('content/post-detail.html')
def post_detail(request, slug, pk):
    post = get_object_or_404(Post.published_objects.all(), slug=slug, pk=pk)

    return {
        'post': post,
    }


@cache_page(settings.CACHE_DURATION)
@render_to('content/content-list.html')
def review_list(request):
    reviews = Review.published_objects.all()
    lists = List.published_objects.all()
    content = sorted([r for r in reviews] + [l for l in lists], key=lambda c: c.published, reverse=True)

    paginator = Paginator(content, 20)
    page = request.GET.get('page')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    return {
        'content': content,
    }


@cache_page(settings.CACHE_DURATION)
@render_to('content/post-list.html')
def post_list(request):
    content = Post.published_objects.all()

    paginator = Paginator(content, 20)
    page = request.GET.get('page')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    return {
        'content': content,
    }


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

from annoying.decorators import render_to
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page


from .models import BaseContent, Review, Post


@login_required
def preview(request, slug, pk):
    try:
        content = Review.objects.get(slug=slug, pk=pk)
    except Review.DoesNotExist:
        try:
            content = Post.objects.get(slug=slug, pk=pk)
        except Post.DoesNotExist:
            raise Http404

    if isinstance(content, Review):
        context = {'review': content}
        template = 'content/review-detail.html'
    elif isinstance(content, Post):
        context = {'post': content}
        template = 'content/post-detail.html'
    else:
        raise Http404

    return render_to_response(template, context, RequestContext(request))


@cache_page(settings.CACHE_DURATION)
@render_to('content/home.html')
def home(request):
    # pinned content
    pinned_content = Review.published_objects.all()[:4]
    excluded_reviews = [content.pk for content in pinned_content] or None
    exclusion_mapping = {
        Review: excluded_reviews,
        Post: None,
    }

    # list of content
    content = BaseContent.get_all_published(limit=15, exclusion_mapping=exclusion_mapping)

    return {
        'pinned_content': pinned_content,
        'content': content,
    }


@cache_page(settings.CACHE_DURATION)
@render_to('content/review-detail.html')
def review_detail(request, slug, pk):
    review = get_object_or_404(Review.published_objects.all(), slug=slug, pk=pk)

    return {
        'review': review,
        'chart_object': review.get_chart_object(),
    }


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
    content = Review.published_objects.all()

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
@render_to('content/content-list.html')
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

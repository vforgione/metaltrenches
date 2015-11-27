from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    # admin
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^preview/(?P<slug>[\w\-]+)-(?P<pk>\d+)/?$', 'metaltrenches.apps.content.views.preview', name='preview'),

    # flat pages
    url(r'^contact/?$', TemplateView.as_view(template_name='base/flat-pages/contact.html'), name='contact'),

    # home
    url(r'^$', 'metaltrenches.apps.content.views.home', name='home'),

    # review detail
    url(r'^reviews/(?P<slug>[\w\-]+)-(?P<pk>\d+)/?$',
        'metaltrenches.apps.content.views.review_detail',
        name='review-detail'),

    # post detail
    url(r'^posts/(?P<slug>[\w\-]+)-(?P<pk>\d+)/?$',
        'metaltrenches.apps.content.views.post_detail',
        name='post-detail'),

    # content lists
    url(r'^reviews/?$', 'metaltrenches.apps.content.views.review_list', name='review-list'),
    url(r'^posts/?$', 'metaltrenches.apps.content.views.post_list', name='post-list'),

    # genres
    url(r'^genres/?$', 'metaltrenches.apps.content.views.genre_list', name='genre-list'),

    # bands
    url(r'^bands/?$', 'metaltrenches.apps.content.views.band_list', name='band-list'),
    url(r'^bands/(?P<slug>[\w\-]+)-(?P<pk>\d+)/?$',
        'metaltrenches.apps.content.views.band_detail',
        name='band-detail'),

    # albums
    url(r'^albums/?$', 'metaltrenches.apps.content.views.album_list', name='album-list'),
    url(r'^albums/(?P<slug>[\w\-]+)-(?P<pk>\d+)/?$',
        'metaltrenches.apps.content.views.album_detail',
        name='album-detail'),

    # events
    url(r'^events/?$', 'metaltrenches.apps.content.views.event_list', name='event-list'),
]

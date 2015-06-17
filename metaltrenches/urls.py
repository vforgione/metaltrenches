from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    # admin
    url(r'^motherfuckingdjadminbitch/', include(admin.site.urls)),  # security by obscurity

    # home
    url(r"^$", "metaltrenches.apps.reviews.views.home", name="home"),

    # reviews
    url(r"^reviews/?$", "metaltrenches.apps.reviews.views.review_list", name="review-list"),
    url(r"^reviews/(?P<slug>[\w\-]+)-(?P<pk>\d+)/?$", "metaltrenches.apps.reviews.views.review_detail", name="review-detail"),
    url(r"^preview/(?P<pk>\d+)/?", "metaltrenches.apps.reviews.views.preview_review", name="review-preview"),

    # bands
    url(r"^bands/?$", "metaltrenches.apps.music.views.band_list", name="band-list"),
    url(r"^bands/(?P<slug>[\w\-]+)/?$", "metaltrenches.apps.music.views.band_detail", name="band-detail"),

    # albums
    url(r"^albums/?$", "metaltrenches.apps.music.views.album_list", name="album-list"),
    url(r"^albums/(?P<slug>[\w\-]+)/?$", "metaltrenches.apps.music.views.album_detail", name="album-detail"),
    
    # search
    url(r"^search/?$", "metaltrenches.apps.reviews.views.search", name="search"),

    # static pages
    url(r"^contact/?$", TemplateView.as_view(template_name='base/contact.html'), name='contact'),
]

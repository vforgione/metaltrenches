from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # admin
    url(r'^admin/', include(admin.site.urls)),

    # home
    url(r"^$", "metaltrenches.apps.reviews.views.home", name="home"),

    # reviews
    url(r"^reviews$", "metaltrenches.apps.reviews.views.review_list", name="review-list"),
    url(r"^reviews/(?P<slug>[\w\-]+)-(?P<pk>\d+)$", "metaltrenches.apps.reviews.views.review_detail", name="review-detail"),

    # bands
    url(r"^bands$", "metaltrenches.apps.reviews.views.band_list", name="band-list"),

    # albums
    url(r"^albums$", "metaltrenches.apps.reviews.views.album_list", name="album-list"),
]

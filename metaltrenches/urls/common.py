from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # admin
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^preview/(?P<slug>[\w\-]+)-(?P<pk>\d+)/?$',
        'metaltrenches.apps.content.views.preview',
        name='preview'),

    # home
    url(r'^$', 'metaltrenches.apps.content.views.home', name='home'),
]

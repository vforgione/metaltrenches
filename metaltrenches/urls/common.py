from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # admin
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

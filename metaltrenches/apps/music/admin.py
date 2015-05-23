from django.contrib import admin

from .models import Genre, Band, Album


admin.site.register(Genre)
admin.site.register(Band)
admin.site.register(Album)

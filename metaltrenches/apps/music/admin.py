from django import forms
from django.contrib import admin
from django.db import models

from .models import Genre, Band, Album, Event


class GenreAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)


class BandAdmin(admin.ModelAdmin):
    ordering = 'name'
    search_fields = ('name',)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'band', 'release_date')
    list_filter = ('release_date',)
    ordering = ('title',)
    search_fields = ('title', 'band', 'release_date')


class EventAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor', 'rows': '50'})},
    }

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


admin.site.register(Genre, GenreAdmin)
admin.site.register(Band, BandAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Event, EventAdmin)

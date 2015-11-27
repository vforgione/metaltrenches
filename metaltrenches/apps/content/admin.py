from django import forms
from django.contrib import admin
from django.contrib.admin.options import StackedInline
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.urlresolvers import reverse
from django.db import models

from .models import Genre, Band, Album, Event, RatingFactor, Rating, Post, Review, List, ListItem


def get_preview_link(admin_class, instance):
    """generates a private link for previewing content - avoids published_objects filter, enforces logged in
    """
    return reverse('preview', kwargs={'slug': instance.slug, 'pk': instance.pk})


class RatingAdminInline(GenericTabularInline):
    model = Rating
    extra = 3


class RatingAdmin(admin.ModelAdmin):
    autocomplete_lookup_fields = {
        'generic': [
            ['content_type', 'object_id'],
        ]
    }
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor', 'rows': '50'})},
    }

    class Media(object):
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class GenreAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)


class BandAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
    inlines = (RatingAdminInline,)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'band', 'release_date')
    list_filter = ('release_date',)
    ordering = ('title',)
    search_fields = ('title', 'band', 'release_date')
    inlines = (RatingAdminInline,)


class EventAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
    inlines = (RatingAdminInline,)
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor', 'rows': '50'})},
    }

    class Media(object):
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'published'
    list_display = ('title', 'published')
    list_filter = ('published',)
    ordering = ('-id',)
    search_fields = ('title', 'subtitle', 'published')
    # view_on_site = get_preview_link
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor', 'rows': '50'})},
    }

    class Media(object):
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class ReviewAdmin(admin.ModelAdmin):
    date_hierarchy = 'published'
    list_display = ('title', 'published', 'subject')
    list_filter = ('published',)
    ordering = ('-id',)
    search_fields = ('title', 'subtitle', 'published')
    # view_on_site = get_preview_link
    autocomplete_lookup_fields = {
        'generic': [
            ['content_type', 'object_id'],
        ]
    }
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor', 'rows': '50'})},
    }

    class Media(object):
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class ListItemAdmin(admin.ModelAdmin):
    list_display = ('list', 'sequence', 'subject')
    ordering = ('list', 'sequence')
    search_fields = ('list', 'subject')
    autocomplete_lookup_fields = {
        'generic': [
            ['content_type', 'object_id'],
        ]
    }
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor', 'rows': '50'})},
    }

    class Media(object):
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class ListItemInlineAdmin(StackedInline):
    model = ListItem
    extra = 3
    autocomplete_lookup_fields = {
        'generic': [
            ['content_type', 'object_id'],
        ]
    }
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor', 'rows': '50'})},
    }

    class Media(object):
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class ListAdmin(admin.ModelAdmin):
    date_hierarchy = 'published'
    list_display = ('title', 'published')
    list_filter = ('published',)
    ordering = ('-id',)
    search_fields = ('title', 'subtitle', 'published')
    inlines = (ListItemInlineAdmin,)
    # view_on_site = get_preview_link


admin.site.register(Genre, GenreAdmin)
admin.site.register(Band, BandAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(RatingFactor)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(ListItem, ListItemAdmin)

from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models

from .models import Post, ReviewItem, Review, RatingFactor, Rating


def get_preview_link(admin_class, instance):
    """generates a private link for previewing content - avoids published_objects filter, enforces logged in
    """
    return reverse('preview', kwargs={'slug': instance.slug, 'pk': instance.pk})


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 3


class ReviewItemAdmin(admin.ModelAdmin):
    inlines = [RatingInline]
    autocomplete_lookup_fields = {
        'generic': [
            ['content_type', 'object_id'],
        ]
    }


class ReviewAdmin(admin.ModelAdmin):
    autocomplete_lookup_fields = {
        'fk': ['subject'],
    }
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor', 'rows': '50'})},
    }
    view_on_site = get_preview_link

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor', 'rows': '50'})},
    }
    view_on_site = get_preview_link

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


admin.site.register(Post, PostAdmin)
admin.site.register(ReviewItem, ReviewItemAdmin)
admin.site.register(RatingFactor)
admin.site.register(Rating)
admin.site.register(Review, ReviewAdmin)

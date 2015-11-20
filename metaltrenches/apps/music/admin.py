from django import forms
from django.contrib import admin
from django.db import models

from .models import Genre, Band, Album, Event


class EventAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'mceEditor', 'rows': '50'})},
    }

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


admin.site.register(Genre)
admin.site.register(Band)
admin.site.register(Album)
admin.site.register(Event, EventAdmin)

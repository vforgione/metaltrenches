from django.contrib import admin

from .models import Rating, RatingFactor


admin.site.register(Rating)
admin.site.register(RatingFactor)

from django.contrib import admin

from .models import RatingFactor, Rating, Review


admin.site.register(RatingFactor)
admin.site.register(Rating)
admin.site.register(Review)

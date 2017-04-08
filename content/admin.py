from django.contrib import admin

from .models import List, ListItem, Post, Review


admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(Post)
admin.site.register(Review)

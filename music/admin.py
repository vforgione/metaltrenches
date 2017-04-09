from django.contrib import admin

from .models import Album, Band, Event, EventPicture, Genre, Person


admin.site.register(Album)
admin.site.register(Band)
admin.site.register(Event)
admin.site.register(EventPicture)
admin.site.register(Genre)
admin.site.register(Person)

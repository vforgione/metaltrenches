from django.conf import settings
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=settings.SLUG_LENGTH, unique=True, blank=True, editable=False)

    class Meta(object):
        app_label = 'music'

    def __str__(self):
        return self.name

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'music:genre-detail', (self.slug, self.pk)

    @property
    def related_albums(self):
        return self.albums.all().order_by('title')

    @property
    def related_bands(self):
        return sorted([album.band for album in self.albums.all()], key=lambda b: b.name)


class Band(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=settings.SLUG_LENGTH, unique=True, blank=True, editable=False)
    picture = models.ImageField(upload_to='band-pictures', null=True, default=None, blank=True)
    website = models.URLField(null=True, default=None, blank=True)
    facebook = models.URLField(null=True, default=None, blank=True)
    twitter = models.URLField(null=True, default=None, blank=True)
    bandcamp = models.URLField(null=True, default=None, blank=True)
    itunes = models.URLField(null=True, default=None, blank=True)
    playstore = models.URLField(null=True, default=None, blank=True)
    amazon = models.URLField(null=True, default=None, blank=True)

    class Meta(object):
        app_label = 'music'

    def __str__(self):
        return self.name

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'music:band-detail', (self.slug,)


class Album(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=settings.SLUG_LENGTH, unique=True, blank=True, editable=False)
    band = models.ForeignKey('music.Band', related_name='albums')
    release_date = models.DateField()
    cover_art = models.ImageField(upload_to='cover-art', null=True, default=None, blank=True)
    genres = models.ManyToManyField('music.Genre', blank=True, related_name='albums')

    class Meta(object):
        app_label = 'music'
        unique_together = (
            ('band', 'title',),
        )

    def __str__(self):
        return '{band}: {title}'.format(band=self.band, title=self.title)

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'music:album-detail', (self.slug, self.pk)


class Event(models.Model):
    name = models.CharField(max_length=255, null=True, default=None, blank=True)
    slug = models.SlugField(max_length=settings.SLUG_LENGTH, unique=True, blank=True, editable=False)
    date = models.DateTimeField(null=True, default=None, blank=True)
    location = models.CharField(max_length=500, null=True, default=None, blank=True)
    bands = models.ManyToManyField('music.Band', related_name='events')
    more_info = models.TextField(null=True, default=None, blank=True)
    picture = models.ImageField(upload_to='event-pictures', null=True, default=None, blank=True)

    class Meta(object):
        app_label = 'music'

    def __str__(self):
        return self.name

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'music:event-detail', (self.slug, self.pk)

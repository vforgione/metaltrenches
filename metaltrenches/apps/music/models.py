from django.conf import settings
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=settings.SLUG_LENGTH, unique=True, blank=True, editable=False)

    class Meta(object):
        app_label = 'music'

    @classmethod
    def get_published_genres(cls):
        from ..content.models import Review
        genres = set()
        for review in Review.published_objects.all():
            for subject in review.subjects.all():
                if isinstance(subject.content_object, Album):
                    for genre in subject.content_object.genres.all():
                        genres.add(genre)
        return genres

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

    @classmethod
    def get_published_bands(cls):
        from ..content.models import Review
        bands = set()
        for review in Review.published_objects.all():
            for subject in review.subjects.all():
                if isinstance(subject.content_object, Album):
                    bands.add(subject.content_object.band)
                elif isinstance(subject.content_object, Band):
                    bands.add(subject.content_object)
                elif isinstance(subject.content_object, Event):
                    for band in subject.content_object.bands.all():
                        bands.add(band)
        return bands

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'band-detail', (self.slug, self.pk)

    def get_detail_image(self):
        if self.picture:
            return self.picture
        for album in self.albums.order_by('-release_date'):
            if album.cover_art:
                return album.cover_art

    def get_reviews(self):
        from ..content.models import Review
        album_pks = [album.pk for album in self.albums.all()]
        event_pks = [event.pk for event in self.events.all()]
        reviews = set()
        for review in Review.published_objects.all():
            for subject in review.subjects.all():
                if isinstance(subject.content_object, Band) and subject.content_object.pk == self.pk:
                    reviews.add(review)
                elif isinstance(subject.content_object, Album) and subject.content_object.pk in album_pks:
                    reviews.add(review)
                elif isinstance(subject.content_object, Event) and subject.content_object.pk in event_pks:
                    reviews.add(review)
        return reviews


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

    @classmethod
    def get_published_albums(cls):
        from ..content.models import Review
        albums = set()
        for review in Review.published_objects.all():
            for subject in review.subjects.all():
                if isinstance(subject.content_object, Album):
                    albums.add(subject.content_object)
        return albums

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

    @classmethod
    def get_published_events(cls):
        from ..content.models import Review
        events = set()
        for review in Review.published_objects.all():
            for subject in review.subjects.all():
                if isinstance(subject.content_object, Event):
                    events.add(subject.content_object)
        return events

    def __str__(self):
        return self.name

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'music:event-detail', (self.slug, self.pk)

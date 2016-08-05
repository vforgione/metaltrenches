import re

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.templatetags.static import StaticNode
from django.utils.html import strip_tags

from .managers import DraftManager, ScheduledManager, PublishedManager


# music stuff

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=settings.SLUG_LENGTH, unique=True, blank=True, editable=False)

    class Meta(object):
        app_label = 'content'
        ordering = ('name',)

    def __str__(self):
        return self.name

    @classmethod
    def get_published_genres(cls):
        genres = set()
        for review in Review.published_objects.all():
            if isinstance(review.subject, Album):
                for genre in review.subject.genres.all():
                        genres.add(genre)
        for list in List.published_objects.all():
            for item in list.items.all():
                if isinstance(item.subject, Album):
                    for genre in item.subject.genres.all():
                        genres.add(genre)
        return genres

    @property
    def related_albums(self):
        return self.albums.all().order_by('title')

    @property
    def related_bands(self):
        return set(sorted([album.band for album in self.albums.all()], key=lambda b: b.name))


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

    reviews = GenericRelation('content.Review')
    list_items = GenericRelation('content.ListItem')
    ratings = GenericRelation('content.Rating')

    class Meta(object):
        app_label = 'content'
        ordering = ('name',)

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'band-detail', (self.slug, self.pk)

    @classmethod
    def get_published_bands(cls):
        bands = set()
        for review in Review.published_objects.all():
            if isinstance(review.subject, Band):
                bands.add(review.subject)
            elif isinstance(review.subject, Album):
                bands.add(review.subject.band)
        for list in List.published_objects.all():
            for item in list.items.all():
                if isinstance(item.subject, Band):
                    bands.add(item.subject)
                elif isinstance(item.subject, Album):
                    bands.add(item.subject.band)
        return bands

    def get_detail_image(self):
        if self.picture:
            return self.picture
        for album in self.albums.all():
            if album.cover_art:
                return album.cover_art
        return ''

    def get_reviews(self):
        album_pks = [album.pk for album in self.albums.all()]
        event_pks = [event.pk for event in self.events.all()]
        reviews = set()
        for review in Review.published_objects.all():
            if isinstance(review.subject, Band) and review.subject.pk == self.pk:
                reviews.add(review)
            elif isinstance(review.subject, Album) and review.subject.pk in album_pks:
                reviews.add(review)
            elif isinstance(review.subject, Event) and review.subject.pk in event_pks:
                reviews.add(review)
        for list in List.published_objects.all():
            for item in list.items.all():
                if isinstance(item.subject, Band) and item.subject.pk == self.pk:
                    reviews.add(list)
                elif isinstance(item.subject, Album) and item.subject.pk in album_pks:
                    reviews.add(list)
                elif isinstance(item.subject, Event) and item.subject.pk in event_pks:
                    reviews.add(list)
        return reviews


class Album(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=settings.SLUG_LENGTH, unique=True, blank=True, editable=False)
    band = models.ForeignKey('content.Band', related_name='albums')
    release_date = models.DateField()
    cover_art = models.ImageField(upload_to='cover-art', null=True, default=None, blank=True)
    genres = models.ManyToManyField(Genre, blank=True, related_name='albums')

    reviews = GenericRelation('content.Review')
    list_items = GenericRelation('content.ListItem')
    ratings = GenericRelation('content.Rating')

    class Meta(object):
        app_label = 'content'
        ordering = ('title',)

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'album-detail', (self.slug, self.pk)

    @classmethod
    def get_published_albums(cls):
        albums = set()
        for review in Review.published_objects.all():
            if isinstance(review.subject, Album):
                albums.add(review.subject)
        for list in List.published_objects.all():
            for item in list.items.all():
                if isinstance(item.subject, Album):
                    albums.add(item.subject)
        return albums

    def get_reviews(self):
        reviews = set()
        for review in Review.published_objects.all():
            if isinstance(review.subject, Album) and review.subject.pk == self.pk:
                reviews.add(review)
        for list in List.published_objects.all():
            for item in list.items.all():
                if isinstance(item.subject, Album) and item.subject.pk == self.pk:
                    reviews.add(list)
        return reviews


class Event(models.Model):
    name = models.CharField(max_length=255, null=True, default=None, blank=True)
    slug = models.SlugField(max_length=settings.SLUG_LENGTH, unique=True, blank=True, editable=False)
    date = models.DateTimeField(null=True, default=None, blank=True)
    location = models.CharField(max_length=500, null=True, default=None, blank=True)
    bands = models.ManyToManyField('content.Band', related_name='events')
    more_info = models.TextField(null=True, default=None, blank=True)
    picture = models.ImageField(upload_to='event-pictures', null=True, default=None, blank=True)

    reviews = GenericRelation('content.Review')
    list_items = GenericRelation('content.ListItem')
    ratings = GenericRelation('content.Rating')

    class Meta(object):
        app_label = 'content'
        ordering = ('name',)

    def __str__(self):
        return self.name

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'event-detail', (self.slug, self.pk)


# content stuff

class RatingFactor(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta(object):
        app_label = 'content'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Rating(models.Model):
    factor = models.ForeignKey('content.RatingFactor')
    score = models.PositiveIntegerField()
    content_type = models.ForeignKey('contenttypes.ContentType', limit_choices_to={'model__in': ('band', 'album', 'event')})
    object_id = models.PositiveIntegerField()
    subject = GenericForeignKey('content_type', 'object_id')

    class Meta(object):
        app_label = 'content'
        ordering = ('-id',)

    def __str__(self):
        return '[{subject}] {factor}:{score}'.format(subject=self.subject, factor=self.factor, score=self.score)


class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255, null=True, default=None, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, editable=False)
    published = models.DateTimeField(null=True, default=None, blank=True)

    class Meta(object):
        abstract = True

    @classmethod
    def get_children(cls):
        return cls.__subclasses__() + [
            grandchild for child in cls.__subclasses__()
            for grandchild in child.get_children()
        ]

    @classmethod
    def get_all_published(cls, limit=100, child_limit=25, exclusion_mapping={}):
        items = []
        for child in cls.get_children():
            excluded_pks = exclusion_mapping.get(child)
            instances = child.published_objects.all()
            if excluded_pks:
                instances = instances.exclude(pk__in=excluded_pks)
            items.extend(instances[:child_limit])
        items = sorted(items, key=lambda x: x.published, reverse=True)
        return items[:limit]

    @classmethod
    def get_all_scheduled(cls, limit=100, child_limit=25, exclusion_mapping={}):
        items = []
        for child in cls.get_children():
            excluded_pks = exclusion_mapping.get(child)
            instances = child.scheduled_objects.all()
            if excluded_pks:
                instances = instances.exclude(pk__in=excluded_pks)
            items.extend(instances[:child_limit])
        items = sorted(items, key=lambda x: x.published, reverse=True)
        return items[:limit]

    @classmethod
    def get_all_draft(cls, limit=100, child_limit=25, exclusion_mapping={}):
        items = []
        for child in cls.get_children():
            excluded_pks = exclusion_mapping.get(child)
            instances = child.draft_objects.all()
            if excluded_pks:
                instances = instances.exclude(pk__in=excluded_pks)
            items.extend(instances[:child_limit])
        items = sorted(items, key=lambda x: x.published, reverse=True)
        return items[:limit]

    def __str__(self):
        return self.title

    def get_detail_image(self):
        return StaticNode.handle_simple('images/logo-white-480x480.png')

    def get_detail_band(self):
        return None

    def get_detail_album(self):
        return None

    def get_short_body(self):
        return re.sub(r'&\w+;', r'', strip_tags(self.body))[:300]


class Post(BaseContent):
    body = models.TextField(default='', blank=True)

    objects = models.Manager()
    published_objects = PublishedManager()
    scheduled_objects = ScheduledManager()
    draft_objects = DraftManager()

    class Meta(object):
        app_label = 'content'
        ordering = ('-id',)

    @models.permalink
    def get_absolute_url(self):
        return 'post-detail', (self.slug, self.pk)


class Review(BaseContent):
    body = models.TextField(default='', blank=True)
    content_type = models.ForeignKey('contenttypes.ContentType', limit_choices_to={'model__in': ('band', 'album', 'event')})
    object_id = models.PositiveIntegerField()
    subject = GenericForeignKey('content_type', 'object_id')

    objects = models.Manager()
    published_objects = PublishedManager()
    scheduled_objects = ScheduledManager()
    draft_objects = DraftManager()

    class Meta(object):
        app_label = 'content'
        ordering = ('-id',)

    @models.permalink
    def get_absolute_url(self):
        return 'review-detail', (self.slug, self.pk)

    def get_detail_image(self):
        if isinstance(self.subject, (Band, Event)):
            return '{media_url}{file_path}'.format(media_url=settings.MEDIA_URL, file_path=self.subject.picture)
        elif isinstance(self.subject, Album):
            return '{media_url}{file_path}'.format(media_url=settings.MEDIA_URL, file_path=self.subject.cover_art)
        else:
            return None

    def get_detail_band(self):
        if isinstance(self.subject, Band):
            return self.subject
        elif isinstance(self.subject, Album):
            return self.subject.band
        elif isinstance(self.subject, Event):
            return self.subject.bands.first()
        return super(Review, self).get_detail_band()

    def get_detail_album(self):
        if isinstance(self.subject, Band):
            return self.subject.albums.last()
        elif isinstance(self.subject, Album):
            return self.subject
        elif isinstance(self.subject, Event):
            band = self.subject.bands.first()
            if band:
                return band.albums.last()
        return super(Review, self).get_detail_band()


class List(BaseContent):
    is_ordered = models.NullBooleanField(default=None, blank=True)
    is_ordered_descending = models.NullBooleanField(default=None, blank=True)
    body = models.TextField(default='', blank=True)

    objects = models.Manager()
    published_objects = PublishedManager()
    scheduled_objects = ScheduledManager()
    draft_objects = DraftManager()

    class Meta(object):
        app_label = 'content'
        ordering = ('-id',)

    @models.permalink
    def get_absolute_url(self):
        return 'review-detail', (self.slug, self.pk)

    def get_detail_image(self):
        subject = self.items.first()
        if subject:
            return subject.get_detail_image()
        super(List, self).get_detail_image()

    def get_detail_band(self):
        subject = self.items.first()
        if subject:
            if isinstance(subject, Band):
                return subject
            elif isinstance(subject, Album):
                return subject.band
            elif isinstance(subject, Event):
                return subject.bands.first()
        return super(List, self).get_detail_band()

    def get_detail_album(self):
        subject = self.items.first()
        if subject:
            if isinstance(subject, Band):
                return subject.albums.last()
            elif isinstance(subject, Album):
                return subject
            elif isinstance(subject, Event):
                band = subject.bands.first()
                if band:
                    return band.albums.last()
        return super(List, self).get_detail_band()

    def get_short_body(self):
        subject = self.items.first()
        if subject:
            return re.sub(r'&\w+;', r'', strip_tags(subject.body))[:300]
        return ''


class ListItem(models.Model):
    list = models.ForeignKey('content.List', related_name='items')
    body = models.TextField(default='', blank=True)
    sequence = models.IntegerField(null=True, default=None, blank=True)
    content_type = models.ForeignKey('contenttypes.ContentType', limit_choices_to={'model__in': ('band', 'album', 'event')})
    object_id = models.PositiveIntegerField()
    subject = GenericForeignKey('content_type', 'object_id')

    class Meta(object):
        app_label = 'content'
        ordering = ('list', 'sequence')

    def __str__(self):
        return str(self.subject)

    def get_detail_image(self):
        if isinstance(self.subject, (Band, Event)):
            return '{media_url}/{file_path}'.format(media_url=settings.MEDIA_URL, file_path=self.subject.picture)
        elif isinstance(self.subject, Album):
            return '{media_url}/{file_path}'.format(media_url=settings.MEDIA_URL, file_path=self.subject.cover_art)
        else:
            return None

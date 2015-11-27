from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models

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

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'genre-detail', (self.slug, self.pk)


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

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'band-detail', (self.slug, self.pk)


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

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'album-detail', (self.slug, self.pk)


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


class Post(BaseContent):
    body = models.TextField(default='', blank=True)

    objects = models.Manager()
    published_objects = PublishedManager()
    scheduled_objects = ScheduledManager()
    draft_objects = DraftManager()

    class Meta(object):
        app_label = 'content'
        ordering = ('-id',)

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'post-detail', (self.slug, self.pk)


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

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'review-detail', (self.slug, self.pk)


class List(BaseContent):
    is_ordered = models.NullBooleanField(default=None, blank=True)
    is_ordered_descending = models.NullBooleanField(default=None, blank=True)

    objects = models.Manager()
    published_objects = PublishedManager()
    scheduled_objects = ScheduledManager()
    draft_objects = DraftManager()

    class Meta(object):
        app_label = 'content'
        ordering = ('-id',)

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'list-detail', (self.slug, self.pk)


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

    def get_detail_image(self):
        if isinstance(self.subject, (Band, Event)):
            return self.subject.picture
        elif isinstance(self.subject, Album):
            return self.subject.cover_art
        else:
            return None

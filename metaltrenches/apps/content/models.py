from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.templatetags.static import StaticNode
from django.utils.functional import cached_property
from django.utils.html import strip_tags

from ..music.models import Band, Album, Event
from .managers import PublishedManager, ScheduledManager, DraftManager


class BaseContent(models.Model):
    class Meta(object):
        abstract = True

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255, null=True, default=None, blank=True)
    body = models.TextField(default='', blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, editable=False)
    published = models.DateTimeField(null=True, default=None, blank=True)

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

    def get_detail_event(self):
        return None

    def get_short_body(self):
        return strip_tags(self.body)[:300]


class Post(BaseContent):
    objects = models.Manager()
    published_objects = PublishedManager()
    scheduled_objects = ScheduledManager()
    draft_objects = DraftManager()

    class Meta(object):
        app_label = 'content'

    @models.permalink
    def get_absolute_url(self):
        return 'post-detail', (self.slug, self.pk)


class ReviewItem(models.Model):
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        null=True,
        default=None,
        blank=True,
        limit_choices_to={'model__in': ('band', 'album', 'event')})
    object_id = models.PositiveIntegerField(null=True, default=None, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    sequence = models.IntegerField(null=True, default=None, blank=True)

    class Meta(object):
        app_label = 'content'

    def __str__(self):
        return str(self.content_object)


class Review(BaseContent):
    subjects = models.ManyToManyField('content.ReviewItem')
    is_ordered = models.NullBooleanField(default=None, blank=True)
    is_ordered_descending = models.NullBooleanField(default=None, blank=True)

    objects = models.Manager()
    published_objects = PublishedManager()
    scheduled_objects = ScheduledManager()
    draft_objects = DraftManager()

    class Meta(object):
        app_label = 'content'

    @models.permalink
    def get_absolute_url(self):
        return 'review-detail', (self.slug, self.pk)

    @cached_property
    def _get_first_subject(self):
        self._first_subject = self.subjects.first()

    @cached_property
    def _get_detail_band_album_event(self):
        self._get_first_subject
        self._detail_band = None
        self._detail_album = None
        self._detail_event = None
        if self._first_subject:
            co = self._first_subject.content_object
            if isinstance(co, Band):
                self._detail_band = co
            elif isinstance(co, Album):
                self._detail_album = co
                self._detail_band = co.band
            elif isinstance(co, Event):
                self._detail_event = co

    def get_detail_image(self):
        self._get_first_subject
        if not self._first_subject:
            return super(Review, self).get_detail_image()

        co = self._first_subject.content_object
        if isinstance(co, (Band, Event)):
            image = co.picture
        elif isinstance(co, Album):
            image = co.cover_art
        else:
            image = None
        if not image:
            return super(Review, self).get_detail_image()

        return '{}{}'.format(settings.MEDIA_URL, image)

    def get_detail_band(self):
        self._get_detail_band_album_event
        return self._detail_band

    def get_detail_album(self):
        self._get_detail_band_album_event
        return self._detail_album

    def get_detail_event(self):
        self._get_detail_band_album_event
        return self._detail_event

    def get_chart_object(self):
        if self.subjects.count() == 1:
            return self.subjects.first()
        return None


class RatingFactor(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta(object):
        app_label = 'content'

    def __str__(self):
        return self.name


class Rating(models.Model):
    item = models.ForeignKey('content.ReviewItem', related_name='ratings')
    factor = models.ForeignKey('content.RatingFactor')
    score = models.IntegerField()

    class Meta(object):
        app_label = 'content'
        unique_together = (
            ('item', 'factor'),
        )

    def __str__(self):
        return '[{item}] {factor}: {score}'.format(item=self.item, factor=self.factor, score=self.score)

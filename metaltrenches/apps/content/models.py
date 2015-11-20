from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

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
    def get_all_published(cls, limit=100, child_limit=25):
        items = []
        for child in cls.get_children():
            items.extend(child.published_objects.all()[:child_limit])
        items = sorted(items, key=lambda x: x.published, reverse=True)
        return items[:limit]

    @classmethod
    def get_all_scheduled(cls, limit=100, child_limit=25):
        items = []
        for child in cls.get_children():
            items.extend(child.scheduled_objects.all()[:child_limit])
        items = sorted(items, key=lambda x: x.published, reverse=True)
        return items[:limit]

    @classmethod
    def get_all_draft(cls, limit=100, child_limit=25):
        items = []
        for child in cls.get_children():
            items.extend(child.draft_objects.all()[:child_limit])
        items = sorted(items, key=lambda x: x.published, reverse=True)
        return items[:limit]

    def __str__(self):
        return self.title


class Post(BaseContent):
    objects = models.Manager()
    published_objects = PublishedManager()
    scheduled_objects = ScheduledManager()
    draft_objects = DraftManager()

    class Meta(object):
        app_label = 'content'

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'post-detail', (self.slug, self.pk)


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

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'review-detail', (self.slug, self.pk)


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

from datetime import datetime
from typing import List

from django.db import models

from .managers import DraftManager, PublishedManager, ScheduledManager


class Content(models.Model):
    class Meta:
        abstract = True

    title: str = models.CharField(max_length=50, unique=True)
    slug: str = models.SlugField(max_length=50, unique=True)
    published: datetime = models.DateTimeField(null=True, default=None, blank=True)
    body: str = models.TextField(default='', blank=True)

    objects = models.Manager()
    daft_objects = DraftManager()
    published_objects = PublishedManager()
    scheduled_objects = ScheduledManager()

    def __str__(self) -> str:
        return self.title

    @classmethod
    def get_children(cls) -> List['Content']:
        return cls.__subclasses__() + [
            grandchild for child in cls.__subclasses__()
            for grandchild in child.get_children()
        ]

    @classmethod
    def get_all_published(cls, limit=100, exclude=None) -> List['Content']:
        exclude = exclude or {}

        items = []
        for child in cls.get_children():
            excluded_pks = exclude.get(child)
            instances = child.published_objects.all()
            if excluded_pks:
                instances = instances.exclude(pk__in=excluded_pks)
            items.extend(instances[:limit])

        items = sorted(items, key=lambda x: x.published, reverse=True)
        return items[:limit]

    @classmethod
    def get_all_scheduled(cls, limit=100, exclude=None) -> List['Content']:
        exclude = exclude or {}

        items = []
        for child in cls.get_children():
            excluded_pks = exclude.get(child)
            instances = child.scheduled_objects.all()
            if excluded_pks:
                instances = instances.exclude(pk__in=excluded_pks)
            items.extend(instances[:limit])

        items = sorted(items, key=lambda x: x.scheduled, reverse=True)
        return items[:limit]

    @classmethod
    def get_all_draft(cls, limit=100, exclude=None) -> List['Content']:
        exclude = exclude or {}

        items = []
        for child in cls.get_children():
            excluded_pks = exclude.get(child)
            instances = child.draft_objects.all()
            if excluded_pks:
                instances = instances.exclude(pk__in=excluded_pks)
            items.extend(instances[:limit])

        items = sorted(items, key=lambda x: x.DRAFT, reverse=True)
        return items[:limit]

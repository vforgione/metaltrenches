from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
            .filter(published__lte=timezone.now()) \
            .exclude(published__isnull=True) \
            .order_by('-published')


class ScheduledManager(models.Manager):
    def get_queryset(self):
        return super(ScheduledManager, self).get_queryset() \
            .filter(published__gt=timezone.now()) \
            .exclude(published__isnull=True) \
            .order_by('published')


class DraftManager(models.Manager):
    def get_queryset(self):
        super(DraftManager, self).get_queryset() \
            .filter(published__isnull=True)

from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return super(PublishedManager, self).get_queryset().filter(published__isnull=False, published__lte=now)


class ScheduledManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return super(ScheduledManager, self).get_queryset().filter(published__isnull=False, published__gt=now)


class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(published__isnull=True)

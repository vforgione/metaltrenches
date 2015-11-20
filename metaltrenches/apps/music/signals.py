from django.db.models.signals import pre_save
from django.dispatch import receiver

from ...utils.signals import make_slug
from .models import Genre, Band, Album, Event


@receiver(pre_save, sender=Genre)
def set_genre_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.name)


@receiver(pre_save, sender=Band)
def set_band_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.name)


@receiver(pre_save, sender=Album)
def set_album_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.title)


@receiver(pre_save, sender=Event)
def set_event_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.name)

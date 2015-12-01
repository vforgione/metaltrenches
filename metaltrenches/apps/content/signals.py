from django.db.models.signals import pre_save
from django.dispatch import receiver

from ...utils.signals import make_slug
from .models import Genre, Band, Album, Event, Post, Review, List


@receiver(pre_save, sender=Genre)
def set_genre_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.name)


@receiver(pre_save, sender=Band)
def set_band_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.name)


@receiver(pre_save, sender=Album)
def set_slbum_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.title)


@receiver(pre_save, sender=Event)
def set_event_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.name)


@receiver(pre_save, sender=Post)
def set_post_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.title)


@receiver(pre_save, sender=Review)
def set_review_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.title)


@receiver(pre_save, sender=List)
def set_list_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.title)

from django.db.models.signals import pre_save
from django.dispatch import receiver

from ...utils.signals import make_slug
from .models import Post, Review


@receiver(pre_save, sender=Post)
def set_post_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.title)


@receiver(pre_save, sender=Review)
def set_review_slug(sender, instance, **kwargs):
    instance.slug = make_slug(instance.title)

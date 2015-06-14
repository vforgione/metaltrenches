from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models

from .managers import PublishedManager, ScheduledManager, DraftManager
from ..music.models import Album
from ..utils import make_slug


class RatingFactor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    album = models.ForeignKey(Album, related_name="ratings")
    factor = models.ForeignKey(RatingFactor)
    score = models.PositiveIntegerField(validators=[MaxValueValidator(10)])

    class Meta(object):
        unique_together = (
            ("album", "factor", ),
        )

    def __str__(self):
        return "[{album}] {factor}: {score}".format(album=self.album, factor=self.factor, score=self.score)


class Review(models.Model):
    # basic fields
    author = models.ForeignKey(User, related_name="reviews")
    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=100, null=True, default=None, blank=True)
    body = models.TextField(default="", blank=True)
    album = models.ForeignKey(Album, related_name="reviews")

    # publishing
    slug = models.SlugField(max_length=100, unique=True, blank=True, editable=False)
    published = models.DateTimeField(null=True, default=None, blank=True)

    # managers
    objects = models.Manager()
    published_objects = PublishedManager()
    scheduled_objects = ScheduledManager()
    draft_objects = DraftManager()

    def save(self, *args, **kwargs):
        self.slug = make_slug(self.title)
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        if self.subtitle:
            return "{title}: {subtitle}".format(title=self.title, subtitle=self.subtitle)
        return self.title

    @models.permalink
    def get_absolute_url(self):
        if self.published is None:
            return "review-preview", (self.pk, )
        return "review-detail", (self.slug, self.pk)

    @property
    def band(self):
        return self.album.band

    @property
    def genres(self):
        return self.album.genres.all()

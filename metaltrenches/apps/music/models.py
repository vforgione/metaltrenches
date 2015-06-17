from django.db import models
from djes.models import Indexable

from .fields import ImageField
from ..utils import make_slug


class Genre(Indexable):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, editable=False)

    class Mapping(object):
        pass

    def save(self, *args, **kwargs):
        self.slug = make_slug(self.name)
        return super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Band(Indexable):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, editable=False)
    website = models.URLField(null=True, default=None, blank=True)
    facebook = models.URLField(null=True, default=None, blank=True)
    twitter = models.URLField(null=True, default=None, blank=True)
    bandcamp = models.URLField(null=True, default=None, blank=True)

    class Mapping(object):
        pass

    def save(self, *args, **kwargs):
        self.slug = make_slug(self.name)
        return super(Band, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return "band-detail", (self.slug, )


class Album(Indexable):
    band = models.ForeignKey(Band, related_name="albums")
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    cover_art = models.ImageField(upload_to="cover-art")
    genres = models.ManyToManyField(Genre, blank=True, related_name="albums")
    slug = models.SlugField(max_length=200, unique=True, blank=True, editable=False)

    class Meta(object):
        unique_together = (
            ("band", "title", "release_date", ),
        )

    class Mapping(object):
        cover_art = ImageField()

    def save(self, *args, **kwargs):
        self.slug = make_slug(self.title)
        return super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return "{band}: {title}".format(band=self.band, title=self.title)

    @models.permalink
    def get_absolute_url(self):
        return "album-detail", (self.slug, )

    def get_genres_string(self):
        return ", ".join([g.name for g in self.genres.all()])

    def get_avg_rating(self):
        ratings = [r for r in self.ratings.all()]
        num_ratings = len(ratings)
        total_score = sum(r.score for r in ratings)
        return round(total_score / num_ratings, 1)

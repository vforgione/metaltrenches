from django.db import models

from ..utils import make_slug


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = make_slug(self.name)
        return super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Band(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, editable=False)
    website = models.URLField(null=True, default=None, blank=True)
    facebook = models.URLField(null=True, default=None, blank=True)
    twitter = models.URLField(null=True, default=None, blank=True)
    bandcamp = models.URLField(null=True, default=None, blank=True)

    def save(self, *args, **kwargs):
        self.slug = make_slug(self.name)
        return super(Band, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return "band-detail", (self.slug, )


class Album(models.Model):
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

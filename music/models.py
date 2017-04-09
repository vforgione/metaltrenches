from datetime import date, datetime
from typing import Iterable

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Genre(models.Model):
    name: str = models.CharField(max_length=30, unique=True)
    slug: str = models.SlugField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.name


class Band(models.Model):
    name: str = models.CharField(max_length=100, unique=True)
    slug: str = models.SlugField(max_length=100, unique=True)
    picture: str = models.ImageField(upload_to='band-pictures', null=True, default=None, blank=True)
    website: str = models.URLField(null=True, default=None, blank=True)
    facebook: str = models.URLField(null=True, default=None, blank=True)
    twitter: str = models.URLField(null=True, default=None, blank=True)
    bandcamp: str = models.URLField(null=True, default=None, blank=True)
    itunes: str = models.URLField(null=True, default=None, blank=True)
    playstore: str = models.URLField(null=True, default=None, blank=True)
    amazon: str = models.URLField(null=True, default=None, blank=True)

    # reverse the generic relationship
    ratings: Iterable['ratings.Rating'] = GenericRelation('ratings.Rating')

    def __str__(self) -> str:
        return self.name


class Album(models.Model):
    title: str = models.CharField(max_length=100)
    slug: str = models.SlugField(max_length=100, unique=True)
    band: Band = models.ForeignKey('music.Band', related_name='albums')
    release_date: datetime = models.DateField()
    cover_art: str = models.ImageField(upload_to='cover-art')
    genres: Iterable[Genre] = models.ManyToManyField('music.Genre', blank=True, related_name='albums')

    # reverse the generic relationship
    ratings: Iterable['ratings.Rating'] = GenericRelation('ratings.Rating')

    def __str__(self) -> str:
        return self.title


class Event(models.Model):
    name: str = models.CharField(max_length=200, unique=True)
    slug: str = models.SlugField(max_length=200, unique=True)
    date: date = models.DateField()
    location: str = models.CharField(max_length=200)
    bands: Iterable[Band] = models.ManyToManyField('music.Band', related_name='events')
    more_info: str = models.TextField(default='')

    # reverse the generic relationship
    ratings: Iterable['ratings.Rating'] = GenericRelation('ratings.Rating')

    def __str__(self) -> str:
        return self.name


class EventPicture(models.Model):
    event: Event = models.ForeignKey('music.Event', related_name='pictures')
    picture: str = models.FileField(upload_to='event-pictures')

    def __str__(self) -> str:
        return f'{self.event} {self.pk}'


class Person(models.Model):
    name: str = models.CharField(max_length=100)
    role: str = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

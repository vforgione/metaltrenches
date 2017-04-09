from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .managers import DraftManager, PublishedManager, ScheduledManager
from .mixins import Content


content_choices = {
    'model__in': ('band', 'album', 'event')
}


class Post(Content):
    objects: models.Manager = models.Manager()
    daft_objects: DraftManager = DraftManager()
    published_objects: PublishedManager = PublishedManager()
    scheduled_objects: ScheduledManager = ScheduledManager()


class Review(Content):
    # these can be related to any number of objects so we're going to use a generic foreign key
    _subject_ctype: ContentType = models.ForeignKey('contenttypes.ContentType', limit_choices_to=content_choices)
    _subject_id: int = models.IntegerField()
    subject: models.Model = GenericForeignKey('_subject_ctype', '_subject_id')

    objects: models.Manager = models.Manager()
    daft_objects: DraftManager = DraftManager()
    published_objects: PublishedManager = PublishedManager()
    scheduled_objects: ScheduledManager = ScheduledManager()


class List(Content):
    is_ordered: bool = models.BooleanField(default=True)
    is_ordered_descending: bool = models.BooleanField(default=True)

    objects: models.Manager = models.Manager()
    daft_objects: DraftManager = DraftManager()
    published_objects: PublishedManager = PublishedManager()
    scheduled_objects: ScheduledManager = ScheduledManager()


class ListItem(models.Model):
    list: List = models.ForeignKey('content.List', related_name='items')
    sequence: int = models.PositiveIntegerField(null=True, default=None, blank=True)
    body: str = models.TextField(default='')

    # these can be related to any number of objects so we're going to use a generic foreign key
    _subject_ctype: ContentType = models.ForeignKey('contenttypes.ContentType', limit_choices_to=content_choices)
    _subject_id: int = models.IntegerField()
    subject: models.Model = GenericForeignKey('_subject_ctype', '_subject_id')

    def __str__(self) -> str:
        return f'[{self.list}] {self.sequence} {self.subject}'


class Interview(Content):
    objects: models.Manager = models.Manager()
    daft_objects: DraftManager = DraftManager()
    published_objects: PublishedManager = PublishedManager()
    scheduled_objects: ScheduledManager = ScheduledManager()


class InterviewQA(models.Model):
    interview: Interview = models.ForeignKey('content.Interview', related_name='qas')
    question: str = models.TextField(default='')
    answer: str = models.TextField(default='', blank=True)
    answerer: 'music.Person' = models.ForeignKey('music.Person')
    sequence: int = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.interview} {self.sequence} {self.question}'

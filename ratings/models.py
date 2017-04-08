from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


rating_choices = {
    'model__in': ('band', 'album', 'event')
}


class RatingFactor(models.Model):
    name: str = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name


class Rating(models.Model):
    factor: RatingFactor = models.ForeignKey('ratings.RatingFactor', related_name='ratings')
    score: int = models.PositiveIntegerField()

    # these can be related to any number of objects so we're going to use a generic foreign key
    _subject_ctype: ContentType = models.ForeignKey('contenttypes.ContentType', limit_choices_to=rating_choices)
    _subject_id: int = models.IntegerField()
    subject: models.Model = GenericForeignKey('_subject_ctype', '_subject_id')

    def __str__(self) -> str:
        return f'[{self.subject}] {self.factor} {self.score}'

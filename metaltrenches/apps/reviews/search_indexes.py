from haystack import indexes

from .models import Review


class ReviewIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Review

    def read_queryset(self, using=None):
        return Review.published_objects.all()

import codecs
import json
import os
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.db import transaction
from metaltrenches.apps.content.models import ReviewItem, Review, RatingFactor, Rating
from metaltrenches.apps.music.models import Album


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'dumps', 'reviews.json')
        with codecs.open(path, 'r', encoding='utf8') as fh:
            data = json.load(fh)

        self.stdout.write('parsing file...')

        reviews = []
        rating_factors = []
        ratings = []
        for obj in data:
            if obj['model'] == 'reviews.review':
                reviews.append(obj)
            elif obj['model'] == 'reviews.ratingfactor':
                rating_factors.append(obj)
            elif obj['model'] == 'reviews.rating':
                ratings.append(obj)

        self.stdout.write('found {} reviews. converting...'.format(len(reviews)))

        album_ids = [r['fields']['album'] for r in reviews]
        albums = Album.objects.in_bulk(album_ids)
        album_ctype = ContentType.objects.get_for_model(Album)

        for r in reviews:
            album_id = r['fields']['album']
            album = albums[album_id]
            with transaction.atomic():
                item = ReviewItem(
                    content_type=album_ctype,
                    object_id=album_id,
                    content_object=album)
                item.save()
                review = Review(
                    title=r['fields']['title'],
                    subtitle=r['fields']['subtitle'],
                    body=r['fields']['body'],
                    published=r['fields']['published'],
                    pk=r['pk'])
                review.save()
                review.subjects.add(item)

        self.stdout.write('found {} rating factors. converting...'.format(len(rating_factors)))

        rfs = {}
        for rf in rating_factors:
            rating_factor = RatingFactor(
                name=rf['fields']['name'],
                pk=rf['pk'])
            rating_factor.save()
            rfs[rating_factor.pk] = rating_factor

        self.stdout.write('found {} ratings. converting...'.format(len(ratings)))

        for r in ratings:
            try:
                item = ReviewItem.objects.get(content_type=album_ctype, object_id=r['fields']['album'])
            except ReviewItem.DoesNotExist:
                continue
            except ReviewItem.MultipleObjectsReturned:
                item = ReviewItem.objects.filter(content_type=album_ctype, object_id=r['fields']['album']).last()
            rating = Rating(
                item=item,
                factor=rfs[r['fields']['factor']],
                score=r['fields']['score'])
            rating.save()

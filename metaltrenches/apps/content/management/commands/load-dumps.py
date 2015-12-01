import codecs
import json
import os

from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError

from metaltrenches.apps.content.models import RatingFactor, Rating, Genre, Album, Band, Post, Review


class Command(BaseCommand):
    def handle(self, *args, **options):
        # factors
        self.stdout.write('Loading Rating Factors')
        factor_filename = os.path.join(settings.BASE_DIR, 'dumps', 'factors.json')
        with codecs.open(factor_filename, 'r', encoding='utf8') as fh:
            data = json.load(fh)
            for obj in data:
                factor = RatingFactor(**obj)
                try:
                    factor.save()
                except IntegrityError:
                    pass
        factors = dict([(factor.name, factor) for factor in RatingFactor.objects.all()])

        # genres
        self.stdout.write('Loading Genres')
        genre_filename = os.path.join(settings.BASE_DIR, 'dumps', 'genres.json')
        with codecs.open(genre_filename, 'r', encoding='utf8') as fh:
            data = json.load(fh)
            for obj in data:
                genre = Genre(**obj)
                try:
                    genre.save()
                except IntegrityError:
                    pass
        genres = dict([(genre.name, genre) for genre in Genre.objects.all()])

        # bands
        self.stdout.write('Loading bands')
        band_filename = os.path.join(settings.BASE_DIR, 'dumps', 'bands.json')
        with codecs.open(band_filename, 'r', encoding='utf8') as fh:
            data = json.load(fh)
            for obj in data:
                band = Band(**obj)
                try:
                    band.save()
                except IntegrityError:
                    pass
        bands = dict([(band.name, band) for band in Band.objects.all()])

        # albums
        self.stdout.write('Loading Albums')
        album_filename = os.path.join(settings.BASE_DIR, 'dumps', 'albums.json')
        with codecs.open(album_filename, 'r', encoding='utf8') as fh:
            data = json.load(fh)
            for obj in data:
                band = bands.get(obj['band'])
                if not band:
                    continue
                del obj['band']
                grs = obj['genres']
                del obj['genres']
                album = Album(**obj)
                album.band = band
                try:
                    album.save()
                    for g in grs:
                        genre = genres.get(g)
                        if g:
                            album.genres.add(genre)
                except IntegrityError:
                    pass
        albums = dict([(album.title, album) for album in Album.objects.all()])

        # posts
        self.stdout.write('Loading Posts')
        post_filename = os.path.join(settings.BASE_DIR, 'dumps', 'posts.json')
        with codecs.open(post_filename, 'r', encoding='utf8') as fh:
            data = json.load(fh)
            for obj in data:
                post = Post(**obj)
                try:
                    post.save()
                except IntegrityError:
                    pass

        # reviews
        self.stdout.write('Loading Reviews')
        review_filename = os.path.join(settings.BASE_DIR, 'dumps', 'reviews.json')
        with codecs.open(review_filename, 'r', encoding='utf8') as fh:
            data = json.load(fh)
            for obj in data:
                subjects = obj['subjects']
                if not len(subjects):
                    continue
                subj = subjects[0]
                del obj['subjects']
                del obj['is_ordered']
                del obj['is_ordered_descending']
                review = Review(**obj)
                subject = None
                if subj['type'] == 'album':
                    subject = albums.get(subj['title'])
                elif subj['type'] == 'band':
                    subject = albums.get(subj['name'])
                if not subject:
                    continue
                review.subject = subject
                try:
                    review.save()
                except IntegrityError:
                    continue
                for rat in subj['ratings']:
                    rf = factors.get(rat['name'])
                    if not rf:
                        continue
                    rating = Rating(factor=rf, score=rat['score'], subject=subject)
                    try:
                        rating.save()
                    except IntegrityError:
                        pass

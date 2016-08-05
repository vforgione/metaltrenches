import codecs
import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from metaltrenches.apps.content.models import Genre, Band, Album, Post, Review, List


class Command(BaseCommand):
    def handle(self, *args, **options):
        dirname = os.path.join(settings.BASE_DIR, 'dumps')

        self.stdout.write('Dumping genres... ', ending='')
        num_genres = self.dump_genres(dirname)
        self.stdout.write(num_genres)

        self.stdout.write('Dumping bands... ', ending='')
        num_bands = self.dump_bands(dirname)
        self.stdout.write(num_bands)

        self.stdout.write('Dumping albums... ', ending='')
        num_albums = self.dump_albums(dirname)
        self.stdout.write(num_albums)

    @staticmethod
    def write(filename, serialized_objects):
        with codecs.open(filename, 'w', encoding='utf8') as fh:
            json.dump(serialized_objects, fh)

    def dump_genres(self, dirname):
        genres = Genre.objects.all()
        serialized_genres = [{
            'pk': genre.pk,
            'name': genre.name
        } for genre in genres]

        filename = os.path.join(dirname, 'genres.json')
        self.write(filename, serialized_genres)

        return len(serialized_genres)

    def dump_bands(self, dirname):
        bands = Band.objects.all()
        serialized_bands = [{
            'pk': band.pk,
            'name': band.name,
            'picture': band.picture,
            'website': band.website,
            'facebook': band.facebook,
            'twitter': band.twitter,
            'bandcamp': band.bandcamp,
            'itunes': band.itunes,
            'playstore': band.playstore,
            'amazon': band.amazon,
        } for band in bands]

        filename = os.path.join(dirname, 'bands.json')
        self.write(filename, serialized_bands)

        return len(serialized_bands)

    def dump_albums(self, dirname):
        albums = Album.objects.all()
        serialized_albums = [{
            'pk': album.pk,
            'title': album.title,
            'band': album.band.pk,
            'release_date': album.release_date,
            'cover_art': album.cover_art,
            'genres': [g.pk for g in album.genres],
            'innovation': next(r for r in album.ratings if r.factor.name.lower() == 'innovation').score,
            'musicianship': next(r for r in album.ratings if r.factor.name.lower() == 'musicianship').score,
            'enjoyability': next(r for r in album.ratings if r.factor.name.lower() == 'enjoyability').score,
        } for album in albums]

        filename = os.path.join(dirname, 'albums.json')
        self.write(filename, serialized_albums)

        return len(serialized_albums)

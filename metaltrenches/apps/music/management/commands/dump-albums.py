import codecs
import json
import os
from django.conf import settings
from django.core.management import BaseCommand
from metaltrenches.apps.music.models import Album


class Command(BaseCommand):
    def handle(self, *args, **options):
        # dump file
        filename = os.path.join(settings.BASE_DIR, 'dumps', 'albums.json')

        # get genres
        albums = Album.objects.all()
        data = [{
            'title': a.title,
            'band': a.band.name,
            'release_date': a.release_date.strftime('%Y-%m-%d') or None,
            'cover_art': str(a.cover_art) or None,
            'genres': [g.name for g in a.genres.all()],
        } for a in albums]

        # write dump file
        with codecs.open(filename, 'w', encoding='utf8') as fh:
            fh.write(json.dumps(data))

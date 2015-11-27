import codecs
import json
import os
from django.conf import settings
from django.core.management import BaseCommand
from metaltrenches.apps.music.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        # dump file
        filename = os.path.join(settings.BASE_DIR, 'dumps', 'genres.json')

        # get genres
        genres = Genre.objects.all()
        data = [{'name': g.name} for g in genres]

        # write dump file
        with codecs.open(filename, 'w', encoding='utf8') as fh:
            fh.write(json.dumps(data))

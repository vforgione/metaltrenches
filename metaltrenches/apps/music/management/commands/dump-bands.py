import codecs
import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from metaltrenches.apps.music.models import Band


class Command(BaseCommand):
    def handle(self, *args, **options):
        # dump file
        filename = os.path.join(settings.BASE_DIR, 'dumps', 'bands.json')

        # get genres
        bands = Band.objects.all()
        data = [{
            'name': b.name,
            'picture': str(b.picture) or None,
            'website': b.website,
            'facebook': b.facebook,
            'twitter': b.twitter,
            'bandcamp': b.bandcamp,
            'itunes': b.itunes,
            'playstore': b.playstore,
            'amazon': b.amazon,
        } for b in bands]

        # write dump file
        with codecs.open(filename, 'w', encoding='utf8') as fh:
            fh.write(json.dumps(data))

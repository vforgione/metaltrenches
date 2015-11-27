import codecs
import json
import os
from django.conf import settings
from django.core.management import BaseCommand
from metaltrenches.apps.content.models import RatingFactor


class Command(BaseCommand):
    def handle(self, *args, **options):
        # dump file
        filename = os.path.join(settings.BASE_DIR, 'dumps', 'factors.json')

        # get genres
        rfs = RatingFactor.objects.all()
        data = [{'name': r.name} for r in rfs]

        # write dump file
        with codecs.open(filename, 'w', encoding='utf8') as fh:
            fh.write(json.dumps(data))

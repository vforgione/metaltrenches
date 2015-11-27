import codecs
import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from metaltrenches.apps.content.models import Post


class Command(BaseCommand):
    def handle(self, *args, **options):
        # dump file
        filename = os.path.join(settings.BASE_DIR, 'dumps', 'posts.json')

        # get genres
        posts = Post.objects.all()
        data = [{
            'title': p.title,
            'subtitle': p.subtitle,
            'body': p.body,
            'published': p.published.strftime('%Y-%m-%d') or None,
        } for p in posts]

        # write dump file
        with codecs.open(filename, 'w', encoding='utf8') as fh:
            fh.write(json.dumps(data))

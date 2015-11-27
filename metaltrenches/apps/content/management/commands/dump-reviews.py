import codecs
import json
import os
from django.conf import settings
from django.core.management import BaseCommand
from metaltrenches.apps.content.models import Review
from metaltrenches.apps.music.models import Album, Band


class Command(BaseCommand):
    def handle(self, *args, **options):
        # dump file
        filename = os.path.join(settings.BASE_DIR, 'dumps', 'reviews.json')

        # get genres
        reviews = Review.objects.all()
        data = []
        for r in reviews:
            body = {
                'title': r.title,
                'subtitle': r.subtitle,
                'body': r.body,
                'published': r.published.strftime('%Y-%m-%d') or None,
                'is_ordered': r.is_ordered,
                'is_ordered_descending': r.is_ordered_descending,
                'subjects': [],
            }
            for s in r.subjects.all():
                if isinstance(s.content_object, Album):
                    body['subjects'].append({
                        'type': 'album',
                        'title': s.content_object.title,
                        'sequence': s.sequence,
                        'ratings': [{
                            'name': r.factor.name,
                            'score': r.score
                        } for r in s.ratings.all()]
                    })
                elif isinstance(s.content_object, Band):
                    body['subjects'].append({
                        'type': 'band',
                        'name': s.content_object.name,
                        'sequence': s.sequence,
                        'ratings': [{
                            'name': r.factor.name,
                            'score': r.score
                        } for r in s.ratings.all()]
                    })
            data.append(body)

        # write dump file
        with codecs.open(filename, 'w', encoding='utf8') as fh:
            fh.write(json.dumps(data))

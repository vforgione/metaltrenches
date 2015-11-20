from django.conf import settings
from django.template.defaultfilters import slugify


def make_slug(base):
    slug = slugify(base)[:settings.SLUG_LENGTH]
    while slug.endswith('-'):
        slug = slug[:-1]
    return slug

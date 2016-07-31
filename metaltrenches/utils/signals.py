from django.conf import settings
from django.template.defaultfilters import slugify


def make_slug(base):
    # fuck you, john
    if base.strip() == 'ἀηδής':
        return 'sickening'
    elif base.strip() == '[::]':
        return 'slice'

    slug = slugify(base)[:settings.SLUG_LENGTH]
    while slug.endswith('-'):
        slug = slug[:-1]
    return slug

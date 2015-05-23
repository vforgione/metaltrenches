from django.template.defaultfilters import slugify


MAX_SLUG_LENGTH = 20


def make_slug(value):
    val = slugify(value)[:MAX_SLUG_LENGTH]
    if val.endswith('-'):
        val = val[:-1]
    return val

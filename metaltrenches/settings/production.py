from .common import *


# caches

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': [
            '127.0.0.1:11211',
        ],
        'KEY_PREFIX': 'metaltrenches'
    }
}

CACHE_DURATION = 60 * 10


# databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'metaltrenches',
        'USER': 'metaltrenches',
        'PASSWORD': 'somuchmetal',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


# debug

DEBUG = False

TEMPLATE_DEBUG = False

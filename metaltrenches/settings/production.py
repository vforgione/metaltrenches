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


# logging

ADMINS = (
    ('Vince Forgione', 'the.vincedent@icloud.com'),
)

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'v.forgione@gmail.com'

EMAIL_HOST_PASSWORD = '7h3M0n@R(h'

EMAIL_PORT = 587

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'include_html': True,
        },
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/django/metaltrenches.log'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        'metaltrenches': {
            'handlers': ['logfile'],
            'level': 'WARNING',
            'propagate': True
        },
    },
}

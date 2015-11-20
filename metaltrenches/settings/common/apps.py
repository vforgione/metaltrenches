pre_django_apps = (
    'grappelli',
)

django_apps = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
)

installed_apps = (
    'pipeline',
)

project_apps = (
    'metaltrenches.apps.music',
    'metaltrenches.apps.content',
    'metaltrenches.apps.social',
)

INSTALLED_APPS = pre_django_apps + django_apps + installed_apps + project_apps

PRE_DJANGO_APPS = ()

DJANGO_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)

THIRD_PARTY_APPS = (
    "pipeline",
    "haystack",
)

PROJECT_APPS = (
    "metaltrenches.apps.ads",
    "metaltrenches.apps.music",
    "metaltrenches.apps.reviews",
    "metaltrenches.apps.social",
)

# this is what is actually used to configure project
INSTALLED_APPS = PRE_DJANGO_APPS + DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

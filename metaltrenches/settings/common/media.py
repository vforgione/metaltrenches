import os

from .dirs import BASE_DIR


MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

import os

from .dirs import PROJECT_DIR, BASE_DIR


STATIC_URL = "/static/"

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static"),
    os.path.join(BASE_DIR, "bower_components"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "assets")

STATICFILES_STORAGE = "pipeline.storage.PipelineCachedStorage"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
)

PIPELINE_CSS = {
    "global": {
        "source_filenames": (
            # "fontawesome/css/font-awesome.css",
            "stylesheets/base.css",
        ),
        "output_filename": "css/global.css"
    },
    "bootstrap": {
        "source_filenames": (
            "bootstrap/dist/css/bootstrap.css",
        ),
        "output_filename": "css/bootstrap.css"
    },
}

PIPELINE_JS = {
    "homepage": {
        "source_filenames": (
            "javascript/home-align.js",
        ),
        "output_filename": "js/homepage.js"
    },
    "bootstrap": {
        "source_filenames": (
            # "jquery/dist/jquery.js",
            "bootstrap/dist/js/bootstrap.js",
        ),
        "output_filename": "js/bootstrap.js"
    },
    "highcharts": {
        "source_filenames": (
            "highcharts/highcharts.js",
        ),
        "output_filename": "js/highcharts.js"
    },
}

PIPELINE_CSS_COMPRESSOR = "pipeline.compressors.yuglify.YuglifyCompressor"

PIPELINE_JS_COMPRESSOR = "pipeline.compressors.yuglify.YuglifyCompressor"

PIPELINE_YUGLIFY_BINARY = "./node_modules/yuglify/bin/yuglify"

import os
from .dirs import PROJECT_DIR, BASE_DIR

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
    os.path.join(BASE_DIR, 'bower_components'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE_CSS = {
    'global': {
        'source_filenames': (
            'stylesheets/base/custom-bootstrap.css',
            'stylesheets/base/base.css',
            'stylesheets/base/share-tools.css',
        ),
        'output_filename': 'css/global.css'
    },

    'homepage': {
        'source_filenames': (
            'stylesheets/home/callout.css',
        ),
        'output_filename': 'css/homepage.css'
    },

    'ratings': {
        'source_filenames': (
            'stylesheets/content/ratings-chart.css',
        ),
        'output_filename': 'css/ratings-chart.css'
    },
}

PIPELINE_JS = {
    'bootstrap': {
        'source_filenames': (
            'bootstrap/dist/js/bootstrap.js',
        ),
        'output_filename': 'js/bootstrap.js'
    },

    'highcharts': {
        'source_filenames': (
            'highcharts/highcharts.js',
        ),
        'output_filename': 'js/highcharts.js'
    },
}

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'

PIPELINE_YUGLIFY_BINARY = './node_modules/yuglify/bin/yuglify'

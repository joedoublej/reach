from settings import *

TEMPLATE_DEBUG = True
DEBUG = True

LOCAL = True
CELERY_ALWAYS_EAGER = True

DATABASES['default']['NAME'] = 'reach'
DATABASES['default']['USER'] = 'root'
DATABASES['default']['PASSWORD'] = ''

DEFAULT_LOGGER_DICT = {
    'handlers': ['console'],
    'level': 'DEBUG',
}

BUGSNAG['release_stage'] = "development"

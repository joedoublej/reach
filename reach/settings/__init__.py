"""
Django settings for reach project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from os.path import abspath, dirname, join
import os
import sys
import urlparse

BASE_DIR = dirname(dirname(__file__))
PROJECT_ROOT = abspath(join(dirname(__file__), '../../'))
LOCAL_FILE = lambda *path: join(PROJECT_ROOT, *path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l&4=^61hdb8p_2)77uq275n=l82gqdp*&$+$p2q)c$7b!30kw('

TEMPLATE_DEBUG = False
DEBUG = False
ALLOWED_HOSTS = ['*']

# Development Settings
if os.environ.get('DEVELOPMENT'):
    TEMPLATE_DEBUG = True
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1']

    # Celery
    CELERY_ALWAYS_EAGER = True

    # Logger
    DEFAULT_LOGGER_DICT = {
        'handlers': ['console'],
        'level': 'DEBUG',
    }
else:
    DEFAULT_LOGGER_DICT = {
        'handlers': ['bugsnag'],
        'level': 'INFO'
    }

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'authtools',
    'django_extensions',

    'reachapp'
)

# User
AUTH_USER_MODEL = 'authtools.User'
DEFAULT_PASSWORD = os.environ.get('DEFAULT_USER_PASSWORD')

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'bugsnag.django.middleware.BugsnagMiddleware',
)

ROOT_URLCONF = 'reach.urls'

# Internationalization
SITE_ID = 1
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
MEDIA_URL_WITH_PROTOCOL = '/media/'

# COMPRESS_ENABLED = True
# COMPRESS_URL = MEDIA_URL
# COMPRESS_OFFLINE = True

# Templates
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
urlparse.uses_netloc.append('mysql')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
                    'compress': True}

    }
}

try:
    if os.environ.get('DEVELOPMENT'):
        database_url = os.environ.get('DATABASE_URL')
    else:
        database_url = os.environ.get('CLEARDB_DATABASE_URL')

    url = urlparse.urlparse(database_url)

    # Ensure default database exists.
    DATABASES['default'] = DATABASES.get('default', {})

    # Update with environment configuration.
    DATABASES['default'].update({
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
    })

except Exception:
    print 'Unexpected error:', sys.exc_info()


# Loggers
from bugsnag.handlers import BugsnagHandler

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'handlers': ['null'],
        'level': 'DEBUG',
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'bugsnag': {
            'level': 'WARNING',
            'class': 'bugsnag.handlers.BugsnagHandler',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        'emails': DEFAULT_LOGGER_DICT
    }
}

if os.environ.get('DEVELOPMENT'):
    for logger in LOGGING['loggers']:
        handlers = LOGGING['loggers'][logger]['handlers']
        LOGGING['loggers'][logger]['handlers'] = []
        LOGGING['loggers'][logger]['level'] = 'DEBUG'
        LOGGING['loggers'][logger]['handlers'].append('console')


# Bugsnag
BUGSNAG = {
  "api_key": os.environ.get('BUGSNAG_API_KEY'),
  "project_root": PROJECT_ROOT,
  "notify_release_stages": ["production", "development"]
}

if os.environ.get('DEVELOPMENT'):
    BUGSNAG['release_stage'] = "development"
else:
    BUGSNAG['release_stage'] = "production"

# Email
SERVER_EMAIL = 'Reach <server@reachapp.com>'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

EMAIL_HOST_USER = os.environ.get('MANDRILL_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('MANDRILL_APIKEY')
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = 1

# Celery
# CELERY_IMPORTS = ("tasks", )
CELERY_RESULT_BACKEND = "amqp"
BROKER_URL = os.environ.get('CLOUDAMQP_URL', "amqp://localhost:5672//")
CELERY_TASK_RESULT_EXPIRES = 300

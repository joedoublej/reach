"""
Django settings for reach project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from os.path import abspath, dirname, join
import os

BASE_DIR = dirname(dirname(__file__))
PROJECT_ROOT = abspath(join(dirname(__file__), '../'))
LOCAL_FILE = lambda *path: join(PROJECT_ROOT, *path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l&4=^61hdb8p_2)77uq275n=l82gqdp*&$+$p2q)c$7b!30kw('

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'django_extensions',

    'reachapp'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "bugsnag.django.middleware.BugsnagMiddleware",
)

ROOT_URLCONF = 'reach.urls'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
                    'compress': True}

    }
}

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

# Loggers
from bugsnag.handlers import BugsnagHandler

DEFAULT_LOGGER_DICT = {
    'handlers': ['bugsnag'],
    'level': 'INFO'
}

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

# Bugsnag
BUGSNAG = {
  "api_key": os.environ.get('BUGSNAG_API_KEY'),
  "project_root": PROJECT_ROOT,
  "notify_release_stages": ["production", "development"]
}

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
BROKER_URL = "amqp://localhost:5672//"
CELERY_TASK_RESULT_EXPIRES = 300

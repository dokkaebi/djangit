import sys
import os


# assume we are ./apps/mainsite/settings.py
APPS_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)

from mainsite import TOP_DIR

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'mainsite',
    'djangit',
]


MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
]


TEMPLATE_LOADERS = [
    # try to load jinja2 templates first
    'jingo.Loader',

    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
JINGO_EXCLUDE_APPS = ('admin','registration','debug_toolbar',)


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


STATICFILES_DIRS = [
]

STATIC_ROOT = os.path.join(TOP_DIR, 'static')
MEDIA_ROOT = os.path.join(TOP_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]



ROOT_URLCONF = 'mainsite.urls'

TEMPLATE_DIRS = (
    os.path.join(TOP_DIR, 'templates'),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True


LOG_DIR = os.path.join(TOP_DIR, 'log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'djangit_log': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'djangit.log'),
            'maxBytes': 1024*1024,
            'backupCount': 3,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'djangit.shell': {
            'handlers': ['djangit_log'],
            'level': 'DEBUG',
        }
    }
}




# try to import local_settings if present
try:
    from settings_project import *
    from settings_local import *
except ImportError as e:
    pass

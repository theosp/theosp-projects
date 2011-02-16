# Django settings
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.dirname(__file__) + '/media/'

SITE_URL = ''
MEDIA_URL = '/media'

"""Installs the Google memcache into Django.

By default django tries to import standard memcache module.
Because appengine memcache is API compatible with Python memcache module,
we can trick Django to think it is installed and to use it.

Now you can use CACHE_BACKEND = 'memcached://' in settings.py. IP address
and port number are not required.
"""
import sys
from google.appengine.api import memcache
sys.modules['memcache'] = memcache
CACHE_BACKEND = 'memcached://'

# determine whether we are live or in the SDK
if not os.path.exists(os.path.abspath(os.path.dirname(__file__)) + '/non_gae_indicator'):
    GOOGLE_APP_ENGINE_LIVE = True
else:
    GOOGLE_APP_ENGINE_LIVE = False

ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = '8m!1)+n76gxr(dkt5^3t$xs8$bn-y5xg2%le1qejo5f3rqqfmx'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'urls'

ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    # path should be absolute: example: os.path.dirname(__file__) + '/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
)

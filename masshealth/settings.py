# Django settings for masshealth project.
from django.conf import global_settings as DEFAULT_SETTINGS
import os
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT, PROJECT_NAME = os.path.split(PROJECT_DIR)
def _prel(*args): return os.path.join(PROJECT_DIR, *args)
def _rrel(*args): return os.path.join(PROJECT_ROOT, *args)
def _pmod(*args): return '.'.join((PROJECT_NAME,) + args)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Bill Freeman', 'bfreeman@appropriatesolutions.com'),
    ('Tyrel Souza', 'tsouza@appropriatesolutions.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'masshealth',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = _rrel('htdocs', 'media', '')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = _rrel('htdocs', 'static', '')


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    _rrel('common_static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3=l!*qfg9qo4i-pg586apk=-ki0si2^0rv28+t0q)i=&amp;vrnyo='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'visualizations.context_processors.visualizations',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = _pmod('urls')

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = _pmod('wsgi', 'application')

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    _rrel('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.gis',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'registration',
    'datastories',
    'places',
    'visualizations',
    'programs',
    'heroes',
    'accounts',
    'profiles',
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

LOGIN_REDIRECT_URL = '/my_profile'

FIXTURE_DIRS = ( # Extra fixure dirs, not stored under an ap
    _rrel('fixtures', 'flatpages'),  # flatpages is off under django.contrib
    )

WEAVE_URL = 'http://metrobostondatacommon.org/weave/'

GRAPPELLI_ADMIN_TITLE = 'Healthy Massachusetts'

# Setting FILEBROWSER_DIRECTORY to MEDIA_ROOT is incorrect, see
# comment in .../site-packages/filebrowser/settings.py
# It must be a path relative to MEDIA_ROOT.  It may NOT begin with a
# slash, and, unless it is empty, as below, it must end with a slash.
# Making it an absolute path, like MEDIA_ROOT, messes up the URLs
# generated for the images (as though MEDIA_URL+FILEBROWSER_DIRECTORY
# were used, though that's no the way it works.)
# FILEBROWSER_DIRECTORY = MEDIA_ROOT  # bogus, see above
FILEBROWSER_DIRECTORY = ''

FILEBROWSER_URL_TINYMCE = STATIC_URL + 'libs/tinymce/jscripts/tiny_mce/'
FILEBROWSER_PATH_TINYMCE = os.path.join(STATIC_ROOT,
                                        'libs/tinymce/jscripts/tiny_mce/')

# Django registration requires this.  It is the number of
# days after a new user has registered by which he must
# activate his account.  There is no default.
ACCOUNT_ACTIVATION_DAYS = 5
# DEFAULT_FROM_EMAIL must also be set, and such other EMAIL
# configuration as to enable successful operation of
#   django.contrib.auth.models.User().email_user
# Using the default smtp email backend, this requires
# EMAIL_HOST, the default is 'localhost', which may or may
# not cut it.  The default EMAIL_PORT is probably correct.
# EMAIL_HOST_USER adn EMAIL_HOST_PASSWORD each default to
# an empty string, which may be ok with the default
# EMAIL_HOST.  EMAIL_USE_TLS defaults to false.

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from local_settings import *
except ImportError:
    pass


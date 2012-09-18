# Django settings for masshealth project.A
import os
import geonode
import sys

# GeoNode directory
GEONODE_ROOT = os.path.dirname(geonode.__file__)
# path to project settins file, resolve if link
sfile = __file__
if sfile.endswith('.pyc'): sfile = sfile[:-1]
PROJECT_ROOT = os.path.dirname(os.path.realpath(sfile))

# temporarily add path
#sys.path.append(PROJECT_ROOT)

###########################################################
# SITE SPECIFIC SETTINGS
# Assume development environment. Override in local_settings
###########################################################

SITE_ID = 1
SITENAME = "HealthyMass"
# Change to actual URL
SITEURL = 'http://localhost:8000/'
ROOT_URLCONF = 'masshealth.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = os.path.join('masshealth.wsgi.application')

# Add additional apps here (appended to INSTALLED_APPS)
SITE_APPS = ()

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3=l!*qfg9qo4i-pg586apk=-ki0si2^0rv28+t0q)i=&amp;vrnyo='
REGISTRATION_OPEN = False
ACCOUNT_ACTIVATION_DAYS = 5

ADMINS = (
    ('Bill Freeman', 'bfreeman@appropriatesolutions.com'),
    ('Tyrel Souza', 'tsouza@appropriatesolutions.com'),
)

# Local time zone for this installation. http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment set to same as your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation.
LANGUAGE_CODE = 'en-us'


# Google API key if using Google maps
GOOGLE_API_KEY="ABQIAAAAkofooZxTfcCv9Wi3zzGTVxTnme5EwnLVtEDGnh-lFVzRJhbdQhQgAhB1eT_2muZtc0dl-ZSWrtzmrw"

###########################################################
# MODE SPECIFIC SETTINGS
# These settings assume a development environment.
# For production, override these in settings_local
###########################################################

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# This is a useful 3rd party django app, install separately
DEBUG_TOOLBAR = False

# Default sqlite3 database (flatfile)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT,'development.db'),
        'USER': '',     # Not used with sqlite
        'PASSWORD': '', # Not used with sqlite
        'HOST': '',     # Not used with sqlite
        'PORT': ''      # Not used with sqlite
    }
}
# Datastore settings to make geonode upload vector layers directly to postgis
DB_DATASTORE=False
#DB_DATASTORE_NAME = 'GeoData'
#DB_DATASTORE_DATABASE = #DATABASE_NAME
#DB_DATASTORE_USER = 'ags' #DATABASE_USER
#DB_DATASTORE_PASSWORD = DATABASE_PASSWORD
#DB_DATASTORE_HOST = 'localhost'
#DB_DATASTORE_PORT = 5432
#DB_DATASTORE_TYPE='postgis'

###########################################################
# MAP DEFAULTS
###########################################################

# Where should newly created maps be focused?
DEFAULT_MAP_CENTER = (0,0)
# How tightly zoomed should newly created maps be?
# 0 = entire world;
# maximum zoom is between 12 and 15 (for Google Maps, coverage varies by area)
DEFAULT_MAP_ZOOM = 0

MAP_BASELAYERS = [{
    "source": {
    "ptype":"gxp_wmscsource",
    "url":"/geoserver/wms",
    "restUrl": "/gs/rest"
  }},{
    "source": {"ptype": "gx_olsource"},
    "type":"OpenLayers.Layer",
    "args":["No background"],
    "group":"background",
    "visibility": False,
    "fixed": True
  },{
    "source": { "ptype":"gx_olsource"},
    "type":"OpenLayers.Layer.OSM",
    "args":["OpenStreetMap"],
    "group":"background",
    "visibility": False,
    "fixed": True
  },{
    "source": { "ptype":"gxp_mapquestsource"},
    "name":"osm",
    "group":"background",
    "visibility": True
  },{
    "source": { "ptype":"gxp_mapquestsource"},
    "name":"naip",
    "group":"background",
    "visibility": False
  },{
    "source": {"ptype": "gxp_bingsource"},
    "name": "AerialWithLabels",
    "fixed": True,
    "visibility": False,
    "group": "background",
  },{
    "source": {"ptype": "gxp_mapboxsource"},
  },{
    "source": {"ptype":"gx_olsource"},
    "type":"OpenLayers.Layer.WMS",
    "group":"background",
    "visibility": False,
    "fixed": True,
    "args":[
      "Blue Marble",
      "http://maps.opengeo.org/geowebcache/service/wms",
      {
        "layers":["bluemarble"],
        "format":"image/png",
        "tiled": True,
        "tilesOrigin":[-20037508.34,-20037508.34]
      },
      {"buffer":0}
    ]
}
]

###########################################################
# GeoNode specific settings. Rarely should need changing
###########################################################

# Do not delete the development database when running tests.
os.environ['REUSE_DB'] = "1"
# This is needed for integration tests, they require
# geonode to be listening for GeoServer auth requests.
os.environ['DJANGO_LIFE_TEST_SERVER_ADDRESS'] = 'localhost:8000'

INSTALLED_APPS = (
    # Django bundled apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',

    # Third party apps
    'django_forms_bootstrap',
    'registration',
    'profiles',
    'avatar',
    'dialogos',
    'agon_ratings',
    'taggit',
    'south',

    # GeoNode apps
    'geonode.maps',
    'geonode.layers',
    'geonode.people',
    'geonode.proxy',
    'geonode.security',
    #'geonode.catalogue',

    # MAPC added apps
    'django.contrib.flatpages',
    'django.contrib.gis',
    'django.contrib.markup',
    'grappelli',
    'filebrowser',
    'masshealth.datastories',
    'masshealth.heroes',
    'masshealth.places',
    'masshealth.programs',
    'masshealth.visualizations',
)

# Agon Ratings
AGON_RATINGS_CATEGORY_CHOICES = {
    "maps.Map": {
        "map": "How good is this map?"
    },
    "maps.Layer": {
        "layer": "How good is this layer?"
    },
}

SOUTH_MIGRATION_MODULES = {
    'registration': 'geonode.migrations.registration',
    'avatar': 'geonode.migrations.avatar',
}

# Setting a custom test runner to avoid running the tests for some problematic 3rd party apps
TEST_RUNNER='django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
      '--verbosity=2',
      '--cover-erase',
      '--nocapture',
      '--with-coverage',
      '--cover-package=geonode',
      '--cover-inclusive',
      '--cover-tests',
      '--detailed-errors',
      '--with-xunit',
      '--stop',
# This is very beautiful/usable but requires: pip install rudolf
#      '--with-color',
# The settings below are useful while debugging test failures or errors
#      '--failed',
#      '--pdb-failures',
#      '--stop',
#      '--pdb',
      ]

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'geonode.context_processors.resource_urls',
    # MAPC Added
    'visualizations.context_processors.visualizations',
)

# Directories to search for templates
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT,'templates/'),
    os.path.join(GEONODE_ROOT, 'templates/')
)

# Additional directories which hold static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'common_static/'),
    os.path.join(GEONODE_ROOT, 'static/')
)

# Additional directories for fixtures
FIXTURE_DIRS = (os.path.join(PROJECT_ROOT, 'fixtures'),
                os.path.join(PROJECT_ROOT, 'flatpages'),)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # MAPC added
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

#AUTHENTICATION_BACKENDS = ('geonode.security.auth.GranularBackend',)
AUTH_PROFILE_MODULE = 'people.Contact'

# The username and password for a user that can add and edit layer details on GeoServer
GEOSERVER_CREDENTIALS = "geoserver_admin", SECRET_KEY

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

# temporary hack for https://github.com/MAPC/masshealth/issues/108
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/admin/",
}
LOGIN_REDIRECT_URL = '/admin/'


###########################################################
# Locations of things 
###########################################################

# URL to static web server that serves CSS, uploaded media, javascript, etc.
# for serving from same server or in development, use '/'
ASSETS_URL = '/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT,'htdocs','media')
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = os.path.join(ASSETS_URL,'media/')

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT,'htdocs','static')

# URL that handles the static files like app media.
STATIC_URL = os.path.join(ASSETS_URL,'static/')
#if CLIENT_DEVELOPMENT is True:
#    GEONODE_CLIENT_LOCATION = 'http://localhost:8080/'
    #GEONODE_CLIENT_LOCATION = os.path.join(STATIC_URL,'geonode/')
#else:
    # this needs to be under STATIC_URL
GEONODE_CLIENT_LOCATION = os.path.join(STATIC_URL,'geonode/')

GEONODE_UPLOAD_PATH = MEDIA_ROOT #os.path.join(STATIC_URL, 'uploaded/')

# The FULLY QUALIFIED url to the GeoServer instance for this GeoNode.
#GEOSERVER_BASE_URL = SITEURL + 'geoserver/'
GEOSERVER_BASE_URL = 'http://localhost:8080/geoserver/'

CATALOGUE = {
    'default': {
        # The underlying CSW implementation
        'ENGINE': 'geonode.catalogue.backends.geonetwork',
        # enabled formats
        #'formats': ['DIF', 'Dublin Core', 'FGDC', 'TC211'],
        'FORMATS': ['TC211'],
        # The FULLY QUALIFIED base url to the CSW instance for this GeoNode
        #'url': 'http://localhost/pycsw/trunk/csw.py',
        'URL': SITEURL + 'geonetwork/srv/en/csw',
        #'url': 'http://localhost:8001/deegree-csw-demo-3.0.4/services',
        # login credentials (for GeoNetwork)
        'USER': 'admin',
        'PASSWORD': 'admin'
    }
}

WEAVE_URL = 'http://metrobostondatacommon.org/weave/'

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
if SITE_APPS:
    INSTALLED_APPS += SITE_APPS

if DEBUG_TOOLBAR:
    INTERNAL_IPS = ('127.0.0.1','10.0.0.160')
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )
    INSTALLED_APPS += ('debug_toolbar',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

try:
    from local_settings import *
except ImportError:
    pass

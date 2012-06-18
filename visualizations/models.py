from django.utils.translation import ugettext as _
from django.db import models

from django.core.files.storage import FileSystemStorage
from django.conf import settings

import os

# Visualization XML templates:
#
# These files are designed and uploaded by an administrator.
#
# They are basically XML files, except that they contain some Django
# template systax variable references, so that they can be customized
# with parameters.
#
# This means that they must be "remdered" by the Django template
# engine, rather than just served staticly.
#
# Therefore, they need not (shouldn't) be under MEDIA_ROOT.
#
# We will use the ordinary render_to_response on them from a simple
# view, so they must be in a directory that some template loader
# searches.
#
# By default, the sub-directory of somewhere on the template load path
# uses is "visualizations/XML", but you can set
# VISUALIZATION_TEMPLATES_SUB_PATH in the project settings..
#
# By default, that path is interpreted relative to the last path in
# the TEMPLATE_DIRS project setting.  If there is some reason you
# can't put this path last (such as another app requiring it's path be
# last), you can specify VISUALIZATION_TEMPLATES_DIR, in your project
# settings, but be sure that it is ALSO in TEMPLATES_DIRS if you do
# so.
#
# You can also choose to have the templates subdirectory of the app
# itself used.  Note that apps can be in your python's site-packages
# directory, which your web server probably SHOULD NOT have permission
# to write, so this fallback has limited utility.  To choose this
# behavior you can do any of:
#
#   Specify it in VISUALIZATION_TEMPLATES_DIR.
#
#   Leave TEMPLATE_DIRS empty, and don't specify or use None for
#   VISUALIZATION_TEMPLATES_DIR.
#
#   Specify VISUALIZATION_TEMPLATES_DIR as False.
#
# All this assumes that your project settings TEMPLATE_LOADERS
# includes a suitable loader.

VISUALIZATION_TEMPLATES_SUB_PATH = getattr(settings,
    'VISUALIZATION_TEMPLATES_SUB_PATH',
    "visualizations/XML")
VISUALIZATION_TEMPLATES_DIR = getattr(settings,
    'VISUALIZATION_TEMPLATES_DIR', None)
if VISUALIZATION_TEMPLATES_DIR is None:
    # We presume it is not set, so try for the last of TEMPLATES_DIRS
    try:
        VISUALIZATION_TEMPLATES_DIR = settings.TEMPLATES_DIRS[-1]
    except:
        pass
if not VISUALIZATION_TEMPLATES_DIR:
    # Either we have a non-None false value or we tried and failed to
    # get the last of TEMPLATES_DIRS.  Use the app directory.
    VISUALIZATION_TEMPLATES_DIR = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "templates")

VISUALIZATION_TEMPLATES_STORAGE = FileSystemStorage(
    VISUALIZATION_TEMPLATES_DIR)

class Visualization(models.Model):
    """Hold imformation needed to render Weave visualizations.
    """
    name = models.CharField(_('Name'), max_length=100)
    kind = models.CharField(_('Type'), max_length=100,
                            blank=True, default='', help_text=_(
        'For grouping to make choosing easier in other admin pages.'))
    thumbnail = models.ImageField(
        _('Dummy Image'), upload_to='visualizations/thumbnails/',
        max_length=255, blank=True, default='', help_text=_(
        'If set, may be shown as a stand-in for the Flash, allowing '
        'delayed loading or click to load functionality.'))
    template = models.FileField(
        _('Visualization template'),
        upload_to=VISUALIZATION_TEMPLATES_SUB_PATH,
        storage=VISUALIZATION_TEMPLATES_STORAGE,
        blank=True, default='')

    def __unicode__(self):
        return self.name

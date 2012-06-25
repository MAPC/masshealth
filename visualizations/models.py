from django.utils.translation import ugettext as _
from django.db import models

from django.utils.safestring import mark_safe
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

class Slot(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    visualization = models.ForeignKey(Visualization)
    rank = models.IntegerField(_('Relative order'), default=500)
    new_row = models.BooleanField(_('Starts new row'), default=True,
                                  help_text=_(
        'If turned off this slot is in the same row as the slot '
        'before it in the relative order.  If on, this slot begins '
        'a new row of slots.'))
    title = models.CharField(_('Row title'), max_length=100,
                             blank=True, default='',
                             help_text=_(
        'Ignored if "Starts new row" is off, or if it is blank.  '
        'Otherwise it is displayed as a heading for the row or '
        'section (group of rows begun by this one).'))
    # The first two values below are width and height.
    # Use a string if you need a suffix.  Integers will be turned into
    # strings later.
    # We can append more paramters to the value tuples as we think of
    # them.
    slot_params_by_type = {
        'Table': (707, 100),
        'Chart': (344, 288),
        'Map':   (344, 288)
        }
    SLOT_TYPE_CHOICES = tuple(
        [(n.lower(), n) for n in slot_params_by_type.keys()]
        )
    slot_params_by_type = dict(
        [ (n.lower(), v) for n, v in slot_params_by_type.items() ])
    slot_type = models.CharField(_('Type'), max_length=100,
                                 blank=False, default='table',
                                 choices=SLOT_TYPE_CHOICES)
    SHOWN_ON_CHOICES = (
        ('-not-shown-', '--not-shown--'),
        ('profile', 'Health Profile pages'),
        )
    shown_on = models.CharField(_('Shown on'), max_length=100,
                                blank=False, default='-not-shown-',
                                choices=SHOWN_ON_CHOICES)

    def width(self):
        v = str(self.__class__.slot_params_by_type[self.slot_type][0])
        return mark_safe('"%s"' % v)

    def height(self):
        v = str(self.__class__.slot_params_by_type[self.slot_type][1])
        return mark_safe('"%s"' % v)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('rank',)
        verbose_name = 'Profiel Visualization Slot'

from django.utils.translation import ugettext as _
from django.contrib.gis.db import models

REGION_TYPE_CHOICES = (
    ('cities-and-towns', 'Cities and Towns'),
)

class Place(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    unitid = models.CharField(max_length=20)
    regiontype = models.CharField(
        max_length=100,
        choices=REGION_TYPE_CHOICES,
        default=REGION_TYPE_CHOICES[0][1])
    profile = models.TextField(_('Profile'), blank=True, default='',
                               help_text=_(
        'Shown at the top of the Health Profile page'))
    program_desc = models.TextField(_('Program Description'),
                                    blank=True, default='', help_text=_(
        'Shown at the top of the Health Programs page'))

    datastories = models.ManyToManyField('datastories.Story')

    geometry = models.MultiPolygonField(srid=26986, blank=True, null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.get_regiontype_display())

from django.utils.translation import ugettext as _
from django.contrib.gis.db import models

class Program(models.Model):
    title = models.CharField(max_length=100)
    description =  models.TextField(_('Program Description'),
                                    blank=True, default='')
    date = models.DateTimeField(_('Created'), auto_now_add=True)
    image = models.ImageField(_('Image'),
                              upload_to='programs/img/%y%U',
                              max_length=255,
                              blank=True,
                              default='')
    place = models.ForeignKey('places.Place')

    geometry = models.MultiPointField(_('Where'), null=True, blank=True)

    objects = models.GeoManager()

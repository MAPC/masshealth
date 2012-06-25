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

    geometry = models.PointField(_('Location'), srid=26986, null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return 'Program %s @ %s' % (self.title, self.place.name)


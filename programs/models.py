from django.utils.translation import ugettext as _
from django.contrib.gis.db import models
from django.template.defaultfilters import slugify

class Program(models.Model):
    title = models.CharField(max_length=100)
    description =  models.TextField(_('Program Description'),
                                    blank=True, default='')
    date = models.DateTimeField(_('Created'), auto_now_add=True)
    image = models.ImageField(_('Image'),
                              upload_to='programs/img/%y%U',
                              max_length=255,
                              blank=True,
                              default='',
                              help_text="Image will be shown at 120x80 in map info windwo.")
    place = models.ForeignKey('places.Place')

    icon = models.ForeignKey('programs.Icon', blank=True, null=True)

    geometry = models.PointField(_('Location'), srid=26986, null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return 'Program %s @ %s' % (self.title, self.place.name)

    def save(self, *args, **kwargs):
        # defaults location to place-centroid
        if not self.geometry:
            self.geometry = self.place.geometry.centroid

        super(Program, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "%s#%s" % (self.place.get_absolute_url(), slugify(self.title))

class Icon(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    image = models.ImageField(_('Image'),
                              upload_to='programs/icons/%y%U',
                              max_length=255,
                              blank=True,
                              default='')

    def __unicode__(self):
        return self.name

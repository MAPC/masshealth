from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from visualizations.models import Visualization
    		
class Page(models.Model):
    """A Story page

    Pages always have text, whether you think of it as an
    abstract or a caption.

    Pages may also have a weave visualization OR a an image.
    Any restriction against having both will probably be
    implemented in the admin form definition
    """
    title = models.CharField(_('Title'), max_length=100)
    owner = models.ForeignKey(User, verbose_name=_('owner'),
                              blank=True, null=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    # We might name this "body", if prefered.  But we never
    # have both an abstract and a caption, so it seems
    # wasteful to have two text areas, and neither name
    # seems appropriate for the combined, more generic field.
    #
    # Note: TextFields can hold empty strings, so null=True
    # is not best practice, since it requires the database
    # to be able to store both text and a NULL, see
    # https://docs.djangoproject.com/en/1.4/ref/models/fields/#null
    # Instead specify an empty string as default..
    text = models.TextField(_('Text'), blank=True, default='')
    image = models.ImageField(_('Image'),
                              upload_to='stories/images/%y%U',
                              max_length=255,
                              blank=True,
                              default='')
    visualization = models.ForeignKey(Visualization,
                                      blank=True, null=True)

    def __unicode__(self):
        return '%s by %s' % (self.title,
                             (self.owner.username if self.owner
                              else "<Anonymous>"))

class Story(models.Model):
    """A Data Story.

    Largely a sequence of Page objects, plus some shared metadata.

    The metadata are direct fields here.

    So that Page objects can appear in multiple Story objects, or
    even more than once in a single Story, they are attached via
    a ManyToMany field.  Since the need not have the same ordering
    in all of the stories in which they appear (and especially if
    they appear more than once in a single story), the page position
    is not stored on the Page object, but insteat an explicit join
    table is used for the ManyToMany relationship, and caries the
    page postiion as extra data.
    """
    title = models.CharField(_('Title'), max_length=100)
    slug  = models.SlugField(max_length=100)
    abstract = models.TextField(_('Abstract'), blank=True, default='')

    owner = models.ForeignKey(User, verbose_name=_('owner'),
                              blank=True, null=True)
    last_modified = models.DateTimeField(auto_now_add=True)

    pages = models.ManyToManyField(Page, through='StoryPage')

    places = models.ManyToManyField('places.Place',
                                    related_name='datastories',
                                    blank=True)

    def __unicode__(self):
        return '%s by %s' % (self.title,
                             (self.owner.username if self.owner
                              else "<Anonymous>"))

    class Meta:
        unique_together = (('title', 'owner'),)
        verbose_name = 'Datastory'
        verbose_name_plural = "Datastories"

class StoryPage(models.Model):
    """Join table for Story to Page, carrying page order extra data.

    See the Story model for more information.
    """
    story = models.ForeignKey(Story)
    page = models.ForeignKey(Page)
    page_number = models.IntegerField(_('Page number'))

    def __unicode__(self):
        return u'%s, page %d: %s' % (self.story,
                                     self.page_number,
                                     self.page.title)

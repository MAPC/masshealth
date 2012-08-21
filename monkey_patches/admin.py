"""Nasty things to do to some app's admin.
"""
from django.forms import SelectMultiple
from django.conf import settings
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.admin import site
from django.contrib.flatpages.admin import FlatPage, FlatPageAdmin

class PreSelectDefaultSiteOnCreateSelectMultiple(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            # None in the add form, a list, possibly empty, in
            # the edit form.  So we're adding a new instance here.
            value = [settings.SITE_ID]
        return super(PreSelectDefaultSiteOnCreateSelectMultiple, self
                     ).render(name, value, attrs, choices)

class Flatpagemedia:
    js = (
        '/static/libs/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/js/textareas.js',
    )
    
def flatpages():
    """Hack the sites field widget.
    """
    fpafm = FlatpageForm.Meta
    if getattr(fpafm, 'widgets', None) is None:
        fpafm.widgets = {}
    fpafm.widgets['sites'] = PreSelectDefaultSiteOnCreateSelectMultiple

    site.unregister(FlatPage)
    FlatPageAdmin.Media = Flatpagemedia
    site.register(FlatPage, FlatPageAdmin)

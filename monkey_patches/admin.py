"""Nasty things to do to some app's admin.
"""
from django.forms import SelectMultiple
from django.conf import settings
from django.contrib.flatpages.forms import FlatpageForm

class PreSelectDefaultSiteOnCreateSelectMultiple(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            # None in the add form, a list, possibly empty, in
            # the edit form.  So we're adding a new instance here.
            value = [settings.SITE_ID]
        return super(PreSelectDefaultSiteOnCreateSelectMultiple, self
                     ).render(name, value, attrs, choices)

def flatpages():
    """Hack the sites field widget.
    """
    fpafm = FlatpageForm.Meta
    if getattr(fpafm, 'widgets', None) is None:
        fpafm.widgets = {}
    fpafm.widgets['sites'] = PreSelectDefaultSiteOnCreateSelectMultiple

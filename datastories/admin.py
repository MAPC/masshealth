from models import Story, Page, StoryPage
from django.contrib import admin
from django.forms import ModelForm

import itertools
from django.contrib.admin.widgets import FilteredSelectMultiple
# We need a custom widget to cause all places to be selected
# by default for a new story (default for ManyToManyField is
# broken, see: https://code.djangoproject.com/ticket/2750 .)
# We can't use formfield_overrides in the admin to apply
# the widget, either, since it goes by field type, not by
# field, and there is another ManyToManyField in Story, so
# we also need a custom admin form..
class PreSelectAllFilteredSelectMultipleWidget(FilteredSelectMultiple):
    """Detect when used for a new instance (value is None) and select all."""
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            # Using as an indication that this is add page,
            # as opposed to edit page, which would represent
            # no selections as an empty list.
            value = [v for v, l in itertools.chain(self.choices, choices)]
        return super(PreSelectAllFilteredSelectMultipleWidget, self
                     ).render(name, value, attrs, choices)

class StoryAdminForm(ModelForm):
    class Meta:
        model = Story
        widgets = dict(
           places=PreSelectAllFilteredSelectMultipleWidget('places', False))

class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = dict(slug=['title'])
    form = StoryAdminForm

admin.site.register(Story, StoryAdmin)
admin.site.register(Page)
admin.site.register(StoryPage)

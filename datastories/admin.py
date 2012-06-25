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
    exclude = ('owner',)
    form = StoryAdminForm

# Uncomment the stuff below to automate keeping  creator as owner
# and restricting editing to owner and superuser

#     save_model(self, request, obj, form, change):
#         if not change:
#             obj.owner = request.user
#         super(StoryAdmin, self).save_model(request, obj, form, change)

#     def queryset(self, request):
#         qs = super(StoryAdmin, self).queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(owner=request.user)

#     def has_change_permission(self, request, obj=None):
#         ok = super(StoryAdmin, self).has_change_permission(request, obj)
#         if not ok:
#             return False
#         if obj is None:
#             return True
#         # Not sure I need this:
#         if request.user.is_superuser:
#             return True
#         return request.user.id == obj.owner.id

admin.site.register(Story, StoryAdmin)
admin.site.register(Page)
admin.site.register(StoryPage)

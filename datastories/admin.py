from models import Story, Page, StoryPage
from django.contrib import admin

class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = dict(slug=['title'])
    exclude = ('owner',)

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

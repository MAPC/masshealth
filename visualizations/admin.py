from django.contrib import admin
from models import Visualization, Slot

def slot_type(obj):
    return obj.get_slot_type_display()
slot_type.short_description = 'Type'

def shown_on(obj):
    return obj.get_shown_on_display()
shown_on.short_description = 'Where'

class SlotAdmin(admin.ModelAdmin):
    list_display = ['name', 'rank', 'new_row', 'title', slot_type, shown_on]
    list_editable = ['rank', 'new_row']

admin.site.register(Visualization)

admin.site.register(Slot, SlotAdmin)

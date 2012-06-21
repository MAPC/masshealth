from django.contrib.gis import admin
from models import Program

def place_name(obj):
    return obj.place.name
place_name.short_description = 'Town'

class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', place_name]

admin.site.register(Program, ProgramAdmin)

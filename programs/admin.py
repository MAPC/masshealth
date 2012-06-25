from django.contrib.gis import admin
from models import Program

# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7912100
admin.GeoModelAdmin.default_lat = 5210000
admin.GeoModelAdmin.default_zoom = 9

def place_name(obj):
    return obj.place.name
place_name.short_description = 'Town'

class ProgramAdmin(admin.OSMGeoAdmin):
    list_display = ['title', place_name]

admin.site.register(Program, ProgramAdmin)

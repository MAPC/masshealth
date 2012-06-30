from django.contrib.gis import admin
from models import Program, Icon

try:
    _model_admin = admin.OSMGeoAdmin
except AttributeError:
    _model_admin = admin.ModelAdmin

# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7912100
admin.GeoModelAdmin.default_lat = 5210000
admin.GeoModelAdmin.default_zoom = 9

def place_name(obj):
    return obj.place.name
place_name.short_description = 'Town'

class ProgramAdmin(_model_admin):
    list_display = ['title', place_name]
    
class Commonmedia:
    js = (
        '/static/libs/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/js/textareas.js',
    )


admin.site.register(Program, ProgramAdmin,
    Media = Commonmedia,
    )
admin.site.register(Icon)

from django.contrib.gis import admin
from models import Place

try:
    _model_admin = admin.OSMGeoAdmin
except AttributeError:
    _model_admin = admin.ModelAdmin


class Commonmedia:
    js = (
        '/static/libs/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/js/textareas.js',
    )
    
admin.site.register(Place, _model_admin,
    Media = Commonmedia,
    )

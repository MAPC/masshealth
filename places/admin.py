from django.contrib.gis import admin
from models import Place

try:
    _model_admin = admin.OSMGeoAdmin
except AttributeError:
    _model_admin = admin.ModelAdmin

admin.site.register(Place, _model_admin)

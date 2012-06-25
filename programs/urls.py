from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'programs.views',

    url(r'^geojson/$', 'all_geojson'),
)

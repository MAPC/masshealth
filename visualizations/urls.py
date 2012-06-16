from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'visualizations.views',

    url(r'^xml/(?P<vis_id>\d+)/(?P<place_id>[^/]+)/$', 'visualization_xml'),
)

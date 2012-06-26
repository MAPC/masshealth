from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'visualizations.views',

    url(r'^xml/(?P<vis_id>\d+)/(?P<place_id>\d+)/$', 'visualization_xml'),
    url(r'^ajax/update/thumbnails/$', 'ajax_thumbnails_post'),
)

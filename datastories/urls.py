from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'datastories.views',

    url(r'^(?P<place_slug>[^/]+)/(?P<story_slug>[^/]+)/$', 'story'),
    url(r'^(?P<place_slug>[^/]+)/$', 'story'),
)

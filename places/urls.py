from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'places.views',

    url(r'^summary/(?P<place_slug>[^/]+)/$', 'summary'),
    url(r'^profiles/(?P<place_slug>[^/]+)/$', 'profiles'),
    url(r'^programs/(?P<place_slug>[^/]+)/$', 'programs'),
)

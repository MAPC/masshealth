from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'datastories.views',

    url(r'^(?P<slug>[^/]+)/$', 'story'),
    url(r'^(?P<owner_id>\d+)/(?P<slug>[^/]+)/$', 'story'),
)

from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '', # Putting it here makes emacs indentation helpful.
    # Examples:
    # url(r'^$', 'masshealth.views.home', name='home'),
    # url(r'^masshealth/', include('masshealth.foo.urls')),
    url(r'^story/', include('datastories.urls')),
    url(r'^visualizations/', include('visualizations.urls')),
    url(r'^place/', include('places.urls')),
    url(r'^crossdomain.xml$', 'visualizations.views.crossdomain'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        # One could make the patter depend on MEDIA_URL[1:], but
        # that doesn't work if someone has stuck a full path with
        # "http://" and some DNS name in there.
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            dict(document_root=settings.MEDIA_ROOT)),
    )

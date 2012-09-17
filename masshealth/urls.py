from django.conf.urls import patterns, include, url
from filebrowser.sites import site
from django.conf import settings

# There appears to be an import order bug (probably
# a Django bug) that results in an exception in
# admin.autodiscover().  It involves "lazy"
# relationships, such as the places ManyToMany field
# in the datastories.models.Story model, where the
# related model is specified as a string, such as
# 'places.Place', in this field's definition.
#
# With DEBUG==False, the models will not have already
# been imported by this point, and the string based
# lazy reference will not have been converted to
# a model reference.  If admin.autodiscover() winds
# up processing datastories first, it will mistakenly
# attempt to use the string as though it were a model
# class.
#
# As a work-around, it seems sufficient to import
# places.models here.  A more general solution is
# to force the app model cache to be populated at
# this point (under the development server this is
# done duirng the "Validating models" phase, and is
# apparently also done when DEBUG==True, at least
# in some configurations).  If you need it, it is:
#
# import django.db.models.loading
# if not django.db.models.loading.app_cache_ready():
#     django.db.models.loading.get_app_errors()
#
# (That's roughly what "Validating models" does.)
import places.models
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import geonode.proxy.urls
from monkey_patches import admin as mpa
mpa.flatpages()

urlpatterns = patterns(
    '', # Putting it here makes emacs indentation helpful.
    # Examples:
    # url(r'^$', 'masshealth.views.home', name='home'),
    # url(r'^masshealth/', include('masshealth.foo.urls')),
    url(r'^story/', include('datastories.urls')),
    url(r'^visualizations/', include('visualizations.urls')),
    url(r'^place/', include('places.urls')),
    url(r'^crossdomain.xml$', 'visualizations.views.crossdomain'),
    url(r'^program/', include('programs.urls')),
    url(r'^data/acls/?$', 'geonode.layers.views.layer_acls', name='layer_acls'),
    url(r'^geonode/', include('geonode.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
)

urlpatterns += geonode.proxy.urls.urlpatterns

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        # One could make the patter depend on MEDIA_URL[1:], but
        # that doesn't work if someone has stuck a full path with
        # "http://" and some DNS name in there.
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            dict(document_root=settings.MEDIA_ROOT)),
    )

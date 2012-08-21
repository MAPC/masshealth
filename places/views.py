from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.conf import settings
from django.middleware.csrf import get_token
from django.core.urlresolvers import reverse

from models import Place
from visualizations.models import Slot

GDAL_AVAILABLE = getattr(settings, 'GDAL_AVAILABLE', True)

def summary(request, place_slug):
    place = get_object_or_404(Place, slug=place_slug)
    page_type = "summary"

    u = request.user
    can_update_thumbnails = u.is_active and (u.is_superuser or u.is_staff)
    if can_update_thumbnails:
        csrf_token_value = get_token(request) # Forces cookie generation.
    else:
        csrf_token_value = ''

    return render_to_response(
        'places/summary.html',
        dict(place=place,
             slots = Slot.objects.filter(shown_on='summary'
                                         ).order_by('rank'),
             can_update_thumbnails=can_update_thumbnails,
             csrf_token_value=csrf_token_value,
             page_type=page_type,
             same_place_parts=InOtherPlace.get_split(
        'summary', 'XXX', 'XXX'),
             ),
        context_instance=RequestContext(request))

def profiles(request, place_slug):
    page_type = "profiles"
    try:
      place = Place.objects.transform(4326).get(slug=place_slug)
    except Place.DoesNotExist:
      raise Http404

    u = request.user
    can_update_thumbnails = u.is_active and (u.is_superuser or u.is_staff)
    if can_update_thumbnails:
        csrf_token_value = get_token(request) # Forces cookie generation.
    else:
        csrf_token_value = ''

    return render_to_response(
        'places/profiles.html',
        dict(place=place,
             slots = Slot.objects.filter(shown_on='profile'
                                         ).order_by('rank'),
             can_update_thumbnails=can_update_thumbnails,
             csrf_token_value=csrf_token_value,
             page_type=page_type,
             same_place_parts=InOtherPlace.get_split(
        'profiles', 'XXX', 'XXX'),
             GDAL_AVAILABLE=GDAL_AVAILABLE),
        context_instance=RequestContext(request))

def programs(request, place_slug):
    page_type = "programs"
    place = get_object_or_404(Place, slug=place_slug)
    return render_to_response(
        'places/programs.html',
        dict(place=place,
             page_type=page_type,
             same_place_parts=InOtherPlace.get_split(
        'programs', 'XXX', 'XXX'),
             ),
        context_instance=RequestContext(request))
    
# Class to help us avoid calling reverse too often
class InOtherPlace(object):
    _instances = {}

    def __init__(self, view, *args, **kwargs):
        """Cash a format string for the particular reverse.

        Each param has the name to be used with reverse kwargs as key,
        and a suitable value as the value.  No two values (in one
        call to this constructor) may be the same, and none may match
        any of the fized parts of the url needed to get here.
        """
        assert not (args and kwargs), "InOtherPlace: don't mix args and kwargs"
        self.viewname = view.func_name

        # Calling reverse() must be deferred until later, since
        # this view, among others, can't possibly be ready in
        # the urlconv, since the views.py containing it has yet
        # to finish importing, so it can't yet be reversed.
        # By the time the first request comes along we should
        # be fine.
        self.view = view
        self.args = tuple([str(a) for a in args])
        self.kwargs = dict([ (n, str(v)) for n, v in kwargs])

        self.key = self.make_key(self.viewname, *args, **kwargs)
        self._instances[self.key] = self

    @staticmethod
    def make_key(viewname, *args, **kwargs):
        if kwargs:
            assert not args, "InOtherPlace: don't mix args and kwargs"
            # can't count on order from keywords.  Keyse will be distinct,
            # but might clash with view name, so decorate:
            return frozenset(
                ['v_%s' % viewname] +
                ['k_%s' % k for k in kwargs]
                )
        return (viewname, len(args))

    @property
    def url(self):
        try:
            return self._url
        except AttributeError:
            pass
        if self.kwargs:
            url = reverse(self.view, kwargs=self.kwargs)
            for n, s in self.kwargs:
                url = url.replace(s, '%%(%s)s')
        elif self.args:
            url = reverse(self.view, args=self.args)
            for a in self.args:
                url = url.replace(a, '%s', 1)
        else:
            url = reverse(self.view)
        self._url = url
        return url

    def format_url(self, *args, **kwargs):
        if kwargs:
            return self.url % kwargs
        if args:
            return self.url % args
        return self.url

    @classmethod
    def get_inst(cls, viewname, *args, **kwargs):
        key = cls.make_key(viewname, *args, **kwargs)
        return cls._instances.get(key, cls._default_instance)

    @classmethod
    def get(cls, viewname, *args, **kwargs):
        inst = cls.get_inst(viewname, *args, **kwargs)
        return inst.format_url(*args, **kwargs)

    @classmethod
    def get_split(cls, viewname, splitter, *args, **kwargs):
        return cls.get(viewname, *args, **kwargs).split(splitter)

    def __repr__(self):
        return 'InOtherPlace: %s' % repr(self.key)

# 'XXX' is pretty darned safe, since all the slugs and all the text in
# in the url patterns is lower case.
InOtherPlace._default_instance = InOtherPlace(summary, 'XXX')
InOtherPlace(profiles, 'XXX')
InOtherPlace(programs, 'XXX')

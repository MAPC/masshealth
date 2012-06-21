from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404

from models import Place
from profile_layout import LAYOUT as PROFILE_LAYOUT

def summary(request, place_slug):
    place = get_object_or_404(Place, slug=place_slug)
    return render_to_response('places/summary.html',
                              dict(place=place),
                              context_instance=RequestContext(request))

def profiles(request, place_slug):
    try:
      place = Place.objects.transform(4326).get(slug=place_slug)
    except Place.DoesNotExist:
      raise Http404

    return render_to_response('places/profiles.html',
                              dict(place=place,
                                   visualization_rows=PROFILE_LAYOUT),
                              context_instance=RequestContext(request))

def programs(request, place_slug):
    place = get_object_or_404(Place, slug=place_slug)
    return render_to_response('places/programs.html',
                              dict(place=place),
                              context_instance=RequestContext(request))
    
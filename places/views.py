from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.conf import settings

from models import Place
from visualizations.models import Slot

GDAL_AVAILABLE = getattr(settings, 'GDAL_AVAILABLE', True)

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

    return render_to_response(
        'places/profiles.html',
        dict(place=place,
             slots = Slot.objects.filter(shown_on='profile'
                                         ).order_by('rank'),
             GDAL_AVAILABLE=GDAL_AVAILABLE),
        context_instance=RequestContext(request))

def programs(request, place_slug):
    place = get_object_or_404(Place, slug=place_slug)
    return render_to_response('places/programs.html',
                              dict(place=place),
                              context_instance=RequestContext(request))
    

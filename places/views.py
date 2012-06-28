from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.conf import settings
from django.middleware.csrf import get_token

from models import Place
from visualizations.models import Slot

GDAL_AVAILABLE = getattr(settings, 'GDAL_AVAILABLE', True)

def summary(request, place_slug):
    place = get_object_or_404(Place, slug=place_slug)
    page_type = "summary"
    return render_to_response('places/summary.html',
                              dict(place=place,
                              page_type=page_type,
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
             GDAL_AVAILABLE=GDAL_AVAILABLE),
        context_instance=RequestContext(request))

def programs(request, place_slug):
    page_type = "programs"
    place = get_object_or_404(Place, slug=place_slug)
    return render_to_response('places/programs.html',
                              dict(place=place,
                              page_type=page_type,
                              ),
                              context_instance=RequestContext(request))
    

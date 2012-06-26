from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from models import Visualization
from places.models import Place

def visualization_xml(request, vis_id, place_id):
    visualization = get_object_or_404(Visualization, id=vis_id)
    place = get_object_or_404(Place, id=place_id)

    return render_to_response(
        visualization.template.name,
        dict(regionalunit=place),
        context_instance=RequestContext(request),
        mimetype='application/xml')

def crossdomain(request):
    return render_to_response(
        'visualizations/crossdomain.xml', 
        {}, 
        mimetype='application/xml')

def ajax_thumbnails_post(request):
    # Much more to come.
    return HttpResponse('unimplemented', 'text/plain')

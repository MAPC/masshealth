from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import Visualization
from places.models import Place

def visualization_xml(request, vis_id, place_id):
    visualization = get_object_or_404(Visualization, id=vis_id)
    place = get_object_or_404(Place, id=place_id)

    return render_to_response(
        visualization.name,
        dict(regionalunit=place),
        context_instance=RequestContext(request),
        mimetype='application/xml')


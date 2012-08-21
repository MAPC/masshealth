from django.http import HttpResponse
from django.utils import simplejson
from django.template.defaultfilters import truncatewords

from models import Program

def all_geojson(request):
    """
    Return a GeoJSON representation of all Programs with title, description and image-url properties.
    """

    try:
      programs = Program.objects.transform(4326).all().select_related()
    except Place.DoesNotExist:
      raise Http404

    features = []

    for program in programs:
        # truncatewords
        properties = dict(title=program.title, description=truncatewords(program.description,20), absolute_url=program.get_absolute_url(), map_icon='layer-0')
        if program.image:
            properties['image_url'] = program.image.url
        if program.icon:
            properties['map_icon'] = 'layer-%s' % program.icon.id
        geometry = simplejson.loads(program.geometry.geojson)
        feature = dict(type='Feature', geometry=geometry, properties=properties)
        features.append(feature)

    response = dict(type='FeatureCollection', features=features)
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from models import Visualization
from places.models import Place
from django.views.decorators.csrf import csrf_exempt

import base64
from io import BytesIO
try:
    import json
except ImportError:
    import simplejson as json
try:
    from PIL import Image
except ImportError:
    import Image
from django.core.files.images import ImageFile

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

@csrf_exempt
def ajax_thumbnails_post(request):
    if request.method != 'POST':
        return HttpResponse(
            "HTTP method %r not supported, use 'POST'" % request.method,
            'text/plain',
            status = 405)
    u = request.user
    if not (u.is_active and (u.is_superuser or u.is_staff)):
        return HttpResponse(
            "You must be logged in as a staff member or super user"
            " to post Visualization thumbnail image updates",
            'text/plain',
            status = 401)
    updates = json.loads(request.POST['visualization_thumbnails'])
    errors = []
    count = 0
    for update in updates:
        vid = update.vid
        try:
            vis = Visualization.objects.get(id=vid)
        except Visualization.DoesNotExist:
            errors.append('No Visualization with id %d' % vid)
            continue
        thumb = vis.thumbnail
        imgdata = base64.b64decode(update.img)
        try:
            imgstream = BytesIO(imgdata)
            img = Image.open(imgstream)
            img.verify()  # Check for corrupt PNG
        except ImportError:
            # PIL (or Pillow) isn't properly installed
            raise
        except:
            errors.append(
                'Image data for Visualization with id %d is corrupt' % vid)
            continue
        # Check that image format is 'PNG'??
        # Or do we want to force png on save??
        filename = '%svid%d.%s' % (
            thumb.field.upload_to, vid, img.format.lower())
        outstream = BytesIO()
        img.save(outstream)
        outstream.seek(0)
        imgfile = ImageFile(outstream, filename)
        thumb.save(filename, imgfile)
        outstream.close() # Not sure this is necessary, but can't hurt.

        count += 1  # Success

    resptxt = '%d out of %d thumbnails updated.' % (count, len(updates))
    if errors:
        resptxt = '\n'.join([resptxt] + errors)
    return HttpResponse(resptxt, 'text/plain')

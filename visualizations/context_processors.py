from django.conf import settings
from django.contrib.sites.models import get_current_site

def visualizations(request):
	return dict(WEAVE_URL=settings.WEAVE_URL,
		    CURRENT_SITE=get_current_site(request))

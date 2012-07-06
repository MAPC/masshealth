from django import template
from places.models import Place
from places.views import InOtherPlace

register = template.Library()

# NOTE: assignment_tag is new in Django 1.4
@register.assignment_tag
def places():
    return Place.place_choices()

@register.assignment_tag(takes_context=True)
def non_place_url_parts(context):
    try:
        return context['same_place_parts']
    except KeyError:
        pass
    # _default_instance had better be a town only argument instance.
    # Empty viewname should get the default.
    return InOtherPlace.get_split('', 'XXX', 'XXX')

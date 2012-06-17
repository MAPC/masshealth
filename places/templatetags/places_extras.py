from django import template
from places.models import Place

register = template.Library()

# NOTE: assignment_tag is new in Django 1.4
@register.assignment_tag
def places():
    return Place.place_choices()

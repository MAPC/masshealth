from django import template
from heroes.models import Hero

register = template.Library()

# NOTE: assignment_tag is new in Django 1.4
@register.assignment_tag
def heroes(selector):
    return Hero.objects.filter(show_in=selector, active=True)

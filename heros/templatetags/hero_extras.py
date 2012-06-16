from django import template
from heros.models import Hero

register = template.Library()

# NOTE: assignment_tag is new in Django 1.4
@register.assignment_tag
def heros(selector):
    return Hero.objects.filter(show_in=self.selector, active=True)

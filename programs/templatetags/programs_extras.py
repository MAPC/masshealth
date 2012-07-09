from django import template

from programs.models import Icon

register = template.Library()

@register.assignment_tag
def get_icons(*args):
    return Icon.objects.all()
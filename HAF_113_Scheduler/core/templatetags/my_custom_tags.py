from django import template

register = template.Library()

@register.simple_tag
def addstring(a, b):
    return str(a) + "_" + str(b)
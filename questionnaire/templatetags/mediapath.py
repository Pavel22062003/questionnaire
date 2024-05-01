from django import template

register = template.Library()


@register.filter
def mediapath(value):
    return f'/media/{value}'

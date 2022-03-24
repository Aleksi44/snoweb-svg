from django import template
register = template.Library()


@register.filter
def title_key(title):
    title = title.replace('_', ' ')
    return title.title()

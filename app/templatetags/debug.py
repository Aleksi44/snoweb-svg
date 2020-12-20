from django import template
register = template.Library()


@register.filter
def pdb(item):
    import pdb
    pdb.set_trace()
    return item

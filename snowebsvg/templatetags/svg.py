from django.conf import settings
from django import template
from django.template.loader import get_template
from snowebsvg.models import Svg

register = template.Library()


@register.simple_tag
def svg_inline(token):
    collection_key, group_key, svg_key = token.split('-')
    svg = Svg.objects.get(
        group__collection__key=collection_key,
        group__key=group_key,
        key=svg_key
    )
    # We don't use baked files in DEBUG mode
    if settings.DEBUG:
        return svg.render()

    svg_tpl = get_template("%s/%s.svg" % (
        svg.group.path_build,
        svg.key
    ))
    return svg_tpl.render()

from django import template
from django.template.loader import get_template
from snowebsvg.models import GroupSvg

register = template.Library()


@register.inclusion_tag('snowebsvg/svg_inline.html', takes_context=True)
def svg_inline(context, group_path):
    collection_key, group_key = group_path.split(':')
    group_svg = GroupSvg.objects.get(
        collection__key=collection_key,
        key=group_key
    )
    group_svg_tpl = get_template("%s/group.svg" % group_svg.path_build)
    return {'svg_content': group_svg_tpl.render()}

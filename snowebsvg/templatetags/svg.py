from django import template
from snowebsvg.models import Svg
from snowebsvg import settings

register = template.Library()


@register.simple_tag
def svg_inline(svg_target, theme=None, size=None, variant=None, grid=False):
    if isinstance(svg_target, Svg):
        return svg_target.render_html(theme, size, variant, grid)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_html(theme, size, variant, grid)


@register.simple_tag
def svg_preview(svg_target, theme=None, size=None, variant=None, grid=False):
    if isinstance(svg_target, Svg):
        return svg_target.render_preview(theme, size, variant, grid)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_preview(theme, size, variant, grid)


@register.simple_tag
def svg_django(svg_target, theme=None, size=None, variant=None):
    if isinstance(svg_target, Svg):
        return svg_target.render_django(theme, size, variant)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_django(theme, size, variant)


@register.simple_tag
def collection_styles(collection, theme=None, size=None):
    return collection.render_styles(theme, size)


@register.simple_tag
def svg_stylesheets(*bundles):
    ret = ""
    for bundle in bundles:
        ret += ("<link rel=\"stylesheet\" href=\"%s%s-%s.css\">" % (
            settings.BASE_URL_CSS,
            bundle,
            settings.VERSION
        ))
    return ret

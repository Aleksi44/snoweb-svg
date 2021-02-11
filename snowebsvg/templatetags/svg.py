from django import template
from snowebsvg.models import Svg
from snowebsvg import settings

register = template.Library()


@register.simple_tag
def svg_inline(svg_target, theme=None, width=None, height=None, variant=None, grid=False, klass=None):
    if isinstance(svg_target, Svg):
        return svg_target.render_html(theme, width, height, variant, grid, klass)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_html(theme, width, height, variant, grid, klass)


@register.simple_tag
def svg_preview(svg_target, theme=None, width=None, height=None, variant=None, grid=False):
    if isinstance(svg_target, Svg):
        return svg_target.render_preview(theme, width, height, variant, grid)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_preview(theme, width, height, variant, grid)


@register.simple_tag
def svg_django(svg_target, theme=None, width=None, height=None, variant=None):
    if isinstance(svg_target, Svg):
        return svg_target.render_django(theme, width, height, variant)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_django(theme, width, height, variant)


@register.simple_tag
def collection_styles(collection):
    return collection.render_styles()


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

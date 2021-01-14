from django import template
from snowebsvg.models import Svg

register = template.Library()


@register.simple_tag
def svg_inline(svg_target, theme=None, size=None, grid=False):
    if isinstance(svg_target, Svg):
        return svg_target.render_html(theme, size, grid)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_html(theme, size, grid)


@register.simple_tag
def svg_preview(svg_target, theme=None, size=None, grid=False):
    if isinstance(svg_target, Svg):
        return svg_target.render_preview(theme, size, grid)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_preview(theme, size, grid)


@register.simple_tag
def svg_django(svg_target, theme=None, size=None):
    if isinstance(svg_target, Svg):
        return svg_target.render_django(theme, size)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_django(theme, size)


@register.simple_tag
def collection_styles(collection, theme=None, size=None):
    return collection.render_styles(theme, size)

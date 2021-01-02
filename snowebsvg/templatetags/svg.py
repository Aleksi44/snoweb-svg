from django import template

from snowebsvg import settings
from snowebsvg.models import Svg

register = template.Library()


@register.simple_tag
def svg_inline(svg_target, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE):
    if isinstance(svg_target, Svg):
        return svg_target.render_html(theme, size)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_html(theme, size)


@register.simple_tag
def svg_django(svg_target, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE):
    if isinstance(svg_target, Svg):
        return svg_target.render_django(theme, size)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_django(theme, size)


@register.simple_tag
def collection_styles(collection, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE):
    return collection.render_styles(theme, size)

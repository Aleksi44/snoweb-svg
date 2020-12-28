from django import template

from snowebsvg import settings

register = template.Library()


@register.simple_tag
def svg_inline(svg, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE):
    return svg.render(theme, size)

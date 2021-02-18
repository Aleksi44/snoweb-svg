from django import template
from snowebsvg.models import Svg
from snowebsvg import settings as svg_settings
from django.conf import settings

register = template.Library()

SVG_DEFAULT_THEME = getattr(settings, 'SVG_DEFAULT_THEME', None)
SVG_DEFAULT_WIDTH = getattr(settings, 'SVG_DEFAULT_WIDTH', None)
SVG_DEFAULT_HEIGHT = getattr(settings, 'SVG_DEFAULT_HEIGHT', None)
SVG_DEFAULT_VARIANT = getattr(settings, 'SVG_DEFAULT_VARIANT', None)


@register.simple_tag
def svg_inline(svg_target, theme=SVG_DEFAULT_THEME, width=SVG_DEFAULT_WIDTH, height=SVG_DEFAULT_HEIGHT,
               variant=SVG_DEFAULT_VARIANT, grid=False, klass=None):
    if isinstance(svg_target, Svg):
        return svg_target.render_html(theme, width, height, variant, grid, klass)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_html(theme, width, height, variant, grid, klass)


@register.simple_tag
def svg_preview(svg_target, theme=SVG_DEFAULT_THEME, width=SVG_DEFAULT_WIDTH, height=SVG_DEFAULT_HEIGHT,
                variant=SVG_DEFAULT_VARIANT, grid=False):
    if isinstance(svg_target, Svg):
        return svg_target.render_preview(theme, width, height, variant, grid)
    else:
        svg = Svg()
        svg_composed = svg.key_decomposer(svg_target)
        return svg_composed.render_preview(theme, width, height, variant, grid)


@register.simple_tag
def svg_django(svg_target, theme=SVG_DEFAULT_THEME, width=SVG_DEFAULT_WIDTH, height=SVG_DEFAULT_HEIGHT,
               variant=SVG_DEFAULT_VARIANT):
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
            svg_settings.BASE_URL_CSS,
            bundle,
            svg_settings.VERSION
        ))
    return ret

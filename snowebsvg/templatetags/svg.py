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


# Layout

class SvgLayoutNode(template.Node):

    def __init__(self, nodelist, svg, theme):
        self.nodelist = nodelist
        self.svg = svg
        self.theme = theme

    def render(self, context):
        # theme = self.theme.resolve(context)
        # TODO: add svg/css/theme
        return self.nodelist.render(context)


@register.tag
def svg_layout(parser, token):
    nodelist = parser.parse(('endsvg_layout',))
    parser.delete_first_token()
    try:
        tag_name, key_composer, theme = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires 2 arguments: `svg_key_composer` and `theme`" % token.contents.split()[0]
        )
    if not (key_composer[0] == key_composer[-1] and key_composer[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r first tag's argument should be in quotes" % tag_name
        )
    svg = Svg()
    svg_composed = svg.key_decomposer(key_composer[1:-1])
    return SvgLayoutNode(
        nodelist,
        svg_composed,
        parser.compile_filter(theme),
    )

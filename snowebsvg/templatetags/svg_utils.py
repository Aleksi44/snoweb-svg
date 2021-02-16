from datetime import datetime
from uuid import uuid4

from django import template
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist

register = template.Library()


@register.simple_tag
def scale(scale_x, scale_y=None, x=50, y=50):
    if not scale_y:
        scale_y = scale_x
    x_calc = (1 - scale_x) * x
    y_calc = (1 - scale_y) * y
    return "translate({:.2f}, {:.2f}) scale({:.2f}, {:.2f})".format(
        x_calc,
        y_calc,
        scale_x,
        scale_y
    )


@register.simple_tag
def parse(list_props):
    return [p.split(';') for p in list_props.split(' ')]


@register.filter
def to_int(value):
    return int(value)


@register.simple_tag
def variant_manager(variant=None, svg=None, variant_part='defs'):
    if variant and svg:
        try:
            svg_template = get_template("snowebsvg/common/variants/%s/%s.html" % (
                variant,
                variant_part
            ))
            return svg_template.render({
                'self': svg,
            })
        except TemplateDoesNotExist:
            return ''
    return ''


@register.simple_tag
def unique_id():
    return datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

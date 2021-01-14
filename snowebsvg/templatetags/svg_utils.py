from django import template

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

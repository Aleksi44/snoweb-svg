from django import template
from snowebsvg import settings

register = template.Library()

variants_settings = {
    'default': (
        ('theme_light_primary', '#14253A'),
        ('theme_light_secondary', '#E63946'),
        ('theme_light_tertiary', '#F7F7F7'),
        ('theme_dark_primary', '#F7F7F7'),
        ('theme_dark_secondary', '#E63946'),
        ('theme_dark_tertiary', '#112032'),
        ('theme_light_background_body', '#FFFFFF'),
        ('theme_dark_background_body', 'radial-gradient(ellipse at top, #173049, #020A11)'),
    ),
    'glass': (
        ('theme_light_primary', '#14253A'),
        ('theme_light_secondary', '#F7F7F7'),
        ('theme_light_tertiary', '#F7F7F7'),
        ('theme_dark_primary', '#F7F7F7'),
        ('theme_dark_secondary', '#F7F7F7'),
        ('theme_dark_tertiary', '#F7F7F7'),
        ('theme_light_background_body', 'linear-gradient(to left, #E7C2F4, #80EAEE)'),
        ('theme_dark_background_body', 'linear-gradient(to left, #FA5DE8, #3CB7DC)'),
    )
}


def current_settings(request):
    ret_settings = {}
    for key, value in variants_settings['default']:
        ret_settings[key] = settings_by_key(request, key)
    return ret_settings


@register.simple_tag
def settings_by_key(request, session_key):
    try:
        return request.session['settings'][session_key]
    except KeyError:
        variant = request.session.get('variant', settings.SVG_DEFAULT_VARIANT)
        try:
            variant_conf = dict(variants_settings[variant])
        except KeyError:
            variant_conf = dict(variants_settings['default'])
        if session_key in variant_conf:
            return variant_conf[session_key]
        return ''

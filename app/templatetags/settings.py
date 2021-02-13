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
        ('theme_light_background_body', 'linear-gradient(217deg, rgba(255,0,0,.8), rgba(255,0,0,0) 70.71%),linear-gradient(127deg, rgba(242,214,17,.8), rgba(242,214,17,0) 70.71%),linear-gradient(336deg, rgba(0,0,255,.8), rgba(0,0,255,0) 70.71%);'),
        ('theme_dark_background_body', 'linear-gradient(217deg, rgba(86,193,202,.8), rgba(86,193,202,0) 70.71%),linear-gradient(127deg, rgba(96,144,209,.8), rgba(96,144,209,0) 70.71%),linear-gradient(336deg, rgba(114,58,223,.8), rgba(114,58,223,0) 70.71%);'),
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

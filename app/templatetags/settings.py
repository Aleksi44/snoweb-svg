from django import template
from snowebsvg import settings

register = template.Library()

variants_settings = {
    'default': (
        ('theme_light_primary', '#111827'),
        ('theme_light_secondary', '#D1D5DB'),
        ('theme_light_tertiary', '#E5E7EB'),
        ('theme_dark_primary', '#C9CED8'),
        ('theme_dark_secondary', '#020D21'),
        ('theme_dark_tertiary', '#08233E'),
        ('theme_light_background_body', '#F9FAFB'),
        ('theme_dark_background_body', '#0C3157'),
    ),
    'glass': (
        ('theme_light_primary', '#111827'),
        ('theme_light_secondary', '#FFF'),
        ('theme_light_tertiary', '#FFF'),
        ('theme_dark_primary', '#C9CED8'),
        ('theme_dark_secondary', '#FFF'),
        ('theme_dark_tertiary', '#FFF'),
        ('theme_light_background_body', '#F9FAFB'),
        ('theme_dark_background_body', '#0C3157'),
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

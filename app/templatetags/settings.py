from django import template
from snowebsvg import settings

register = template.Library()

variants_settings = {
    'default': (
        ('theme_light_primary', '#090D49'),
        ('theme_light_secondary', '#65CDAE'),
        ('theme_light_tertiary', '#E5E7EB'),
        ('theme_dark_primary', '#FFF'),
        ('theme_dark_secondary', '#65CDAE'),
        ('theme_dark_tertiary', '#37A987'),
        ('theme_light_background_body', '#F9FAFB'),
        ('theme_dark_background_body', '#090d49'),
    ),
    'glass': (
        ('theme_light_primary', '#111827'),
        ('theme_light_secondary', '#65CDAE'),
        ('theme_light_tertiary', '#D1D5DB'),
        ('theme_dark_primary', '#FFF'),
        ('theme_dark_secondary', '#65CDAE'),
        ('theme_dark_tertiary', '#37A987'),
        ('theme_light_background_body', '#F9FAFB'),
        ('theme_dark_background_body', '#090d49'),
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
    except (KeyError, AttributeError):
        if request:
            variant = request.session.get('variant', settings.SVG_DEFAULT_VARIANT)
        else:
            variant = settings.SVG_DEFAULT_VARIANT
        try:
            variant_conf = dict(variants_settings[variant])
        except KeyError:
            variant_conf = dict(variants_settings['default'])
        if session_key in variant_conf:
            return variant_conf[session_key]
        return ''

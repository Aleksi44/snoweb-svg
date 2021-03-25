from django.core.cache import caches
from django.core.cache.utils import make_template_fragment_key
from django.template import (Library, Node)

from app.templatetags.settings import settings_by_key
from snowebsvg import settings

register = Library()

# 1 year
EXPIRE_TIME = 60 * 60 * 24 * 365


class CachePage(Node):
    def __init__(self, nodelist, request):
        self.nodelist = nodelist
        self.request = request

    def render(self, context):
        fragment_cache = caches['default']
        request = self.request.resolve(context)
        theme = request.session.get('theme', settings.SVG_DEFAULT_THEME)
        variant = request.session.get('variant', settings.SVG_DEFAULT_VARIANT)
        theme_light_primary = settings_by_key(request, 'theme_light_primary')
        theme_light_secondary = settings_by_key(request, 'theme_light_secondary')
        theme_light_tertiary = settings_by_key(request, 'theme_light_tertiary')

        theme_dark_primary = settings_by_key(request, 'theme_dark_primary')
        theme_dark_secondary = settings_by_key(request, 'theme_dark_secondary')
        theme_dark_tertiary = settings_by_key(request, 'theme_dark_tertiary')

        vary_on = list()
        vary_on.append({
            'theme': theme,
            'variant': variant,
            'lang': request.LANGUAGE_CODE,
            'theme_light_primary': theme_light_primary,
            'theme_light_secondary': theme_light_secondary,
            'theme_light_tertiary': theme_light_tertiary,
            'theme_dark_primary': theme_dark_primary,
            'theme_dark_secondary': theme_dark_secondary,
            'theme_dark_tertiary': theme_dark_tertiary
        })
        fragment_name = 'page_%s_%s' % (
            settings.VERSION,
            request.get_full_path()
        )
        cache_key = make_template_fragment_key(fragment_name, vary_on)
        value = fragment_cache.get(cache_key)
        if value is None:
            value = self.nodelist.render(context)
            fragment_cache.set(cache_key, value, EXPIRE_TIME)
        return value


@register.tag
def cache_page(parser, token):
    nodelist = parser.parse(('endcache_page',))
    parser.delete_first_token()
    tokens = token.split_contents()
    return CachePage(
        nodelist,
        parser.compile_filter(tokens[1]),
    )

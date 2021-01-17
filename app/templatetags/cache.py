from django.core.cache import caches
from django.core.cache.utils import make_template_fragment_key
from django.template import (Library, Node)
from django.conf import settings as settings_django

from snowebsvg import settings

register = Library()

# 1 year
EXPIRE_TIME = 60 * 60 * 24 * 365


class CachePage(Node):
    def __init__(self, nodelist, request):
        self.nodelist = nodelist
        self.request = request

    def render(self, context):
        if not settings_django.DEBUG:
            fragment_cache = caches['default']
            request = self.request.resolve(context)
            theme = request.session.get('theme', settings.SVG_DEFAULT_THEME)
            variant = request.session.get('variant', settings.SVG_DEFAULT_VARIANT)
            vary_on = list()
            vary_on.append({
                'theme': theme,
                'variant': variant
            })
            fragment_name = 'page_%s_%s' % (
                settings.VERSION,
                request.path
            )
            cache_key = make_template_fragment_key(fragment_name, vary_on)
            value = fragment_cache.get(cache_key)
            if value is None:
                value = self.nodelist.render(context)
                fragment_cache.set(cache_key, value, EXPIRE_TIME)
            return value
        return self.nodelist.render(context)


@register.tag
def cache_page(parser, token):
    nodelist = parser.parse(('endcache_page',))
    parser.delete_first_token()
    tokens = token.split_contents()
    return CachePage(
        nodelist,
        parser.compile_filter(tokens[1]),
    )

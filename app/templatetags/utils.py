import os
from django import template
from django.conf import settings
from django.template.loader import get_template
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from wand.image import Image
from wand.color import Color
from snowebsvg.settings import SVG_DEFAULT_VARIANT, SVG_DEFAULT_THEME

register = template.Library()


@register.filter
def title_key(title):
    title = title.replace('_', ' ')
    return title.title()


@register.simple_tag(takes_context=True)
def svg_preview_url(context, svg):
    image_preview_path = os.path.join('svg-preview', svg.key_composer + '.png')
    try:
        default_storage.open(image_preview_path, 'r')
        return settings.MEDIA_URL + image_preview_path
    except FileNotFoundError:
        content_svg = get_template(svg.path_entry).render({
            'self': svg,
            'theme': SVG_DEFAULT_THEME,
            'width': 100,
            'height': 100,
            'grid': False,
            'variant': SVG_DEFAULT_VARIANT,
            'css': True,
            'request': context.request
        })
        with Image(blob=content_svg.encode(), format='svg') as img:
            return settings.MEDIA_URL + default_storage.save(
                image_preview_path,
                ContentFile(img.make_blob(format='png'))
            )

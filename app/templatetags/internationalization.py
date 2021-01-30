from django import template

register = template.Library()


@register.filter
def alternate_href(request, lang_code):
    return request.path.replace(
        '/' + request.LANGUAGE_CODE + '/',
        '/' + lang_code + '/'
    )

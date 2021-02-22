from bs4 import BeautifulSoup as bs
from django import template

register = template.Library()


@register.filter
def prettify(html):
    return bs(html, "html.parser").prettify()

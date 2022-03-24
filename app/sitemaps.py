from django.contrib import sitemaps
from django.urls import reverse
from django.contrib.sites.models import Site

from snowebsvg.models import Collection, GroupSvg, Svg


class BaseSitemap(sitemaps.Sitemap):
    priority = 0.4
    protocol = 'https'
    changefreq = 'daily'

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='www.snoweb-svg.com', name='www.snoweb-svg.com')
        return super(BaseSitemap, self).get_urls(site=site, **kwargs)


class CollectionSitemap(BaseSitemap):

    def items(self):
        return Collection.objects.all()

    def location(self, item):
        return reverse('app:svg_search', kwargs={'key': item.key})


class GroupSvgSitemap(BaseSitemap):

    def items(self):
        return GroupSvg.objects.all()

    def location(self, item):
        return reverse('app:svg_search', kwargs={'key': item.key})


class SvgSitemap(BaseSitemap):

    def items(self):
        return Svg.objects.all()

    def location(self, item):
        return reverse('app:svg', kwargs={
            'collection_key': item.group.collection.key,
            'group_key': item.group.key,
            'svg_key': item.key
        })

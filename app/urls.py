from django.contrib.sitemaps.views import sitemap
from django.urls import path

from app.views import CollectionList, GroupSvgList, SvgList, SvgSearch
from app.sitemaps import StaticSitemap, CollectionSitemap, GroupSvgSitemap, SvgSitemap

app_name = 'app'

sitemaps = {
    'static': StaticSitemap,
    'collection': CollectionSitemap,
    'svg': SvgSitemap,
    'group_svg': GroupSvgSitemap,
}

urlpatterns = [
    path('', CollectionList.as_view(), name='collection'),
    path('collection/<collection_key>/', GroupSvgList.as_view(), name='group'),
    path('svg/<collection_key>/<group_key>/<svg_key>/', SvgList.as_view(), name='svg'),
    path('search/', SvgSearch.as_view(), name='svg_search'),
    path('search/<key>/', SvgSearch.as_view(), name='svg_search'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]

from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView

from app.views import \
    CollectionListView, \
    GroupSvgListView, \
    SvgListView, \
    SvgSearchView, \
    SvgSettingsView

from app.sitemaps import \
    StaticSitemap, \
    CollectionSitemap, \
    GroupSvgSitemap, \
    SvgSitemap

app_name = 'app'

sitemaps = {
    'static': StaticSitemap,
    'collection': CollectionSitemap,
    'svg': SvgSitemap,
    'group_svg': GroupSvgSitemap,
}

urlpatterns = [
    path('', CollectionListView.as_view(), name='collection'),
    path('collection/<collection_key>/', GroupSvgListView.as_view(), name='group'),
    path('svg/<collection_key>/<group_key>/<svg_key>/', SvgListView.as_view(), name='svg'),
    path('search/', SvgSearchView.as_view(), name='svg_search'),
    path('search/<key>/', SvgSearchView.as_view(), name='svg_search'),
    path('settings/', SvgSettingsView.as_view(), name='svg_settings'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]

from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse_lazy
from app.views import SvgListView, SvgSearchView, SvgSettingsView
from app.sitemaps import StaticSitemap, CollectionSitemap, SvgSitemap, GroupSvgSitemap

app_name = 'app'

sitemaps = {
    'static': StaticSitemap,
    'collection': CollectionSitemap,
    'group': GroupSvgSitemap,
    'svg': SvgSitemap,
}

urlpatterns = [
    path('', RedirectView.as_view(permanent=True, url=reverse_lazy('app:svg_search')), name='home'),
    path('svg/settings/', SvgSettingsView.as_view(), name='svg_settings'),
    path('svg/', SvgSearchView.as_view(), name='svg_search'),
    path('svg/<key>/', SvgSearchView.as_view(), name='svg_search'),
    path('svg/<collection_key>/<group_key>/<svg_key>/', SvgListView.as_view(), name='svg'),
    path('svg/sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]

from django.urls import path

from app.views import CollectionList, GroupSvgList, SvgList, SvgSearch

app_name = 'app'

urlpatterns = [
    path('', CollectionList.as_view(), name='collection'),
    path('collection/<collection_key>/', GroupSvgList.as_view(), name='group'),
    path('svg/<collection_key>/<group_key>/<svg_key>/', SvgList.as_view(), name='svg'),
    path('search/', SvgSearch.as_view(), name='svg_search'),
    path('search/<key>/', SvgSearch.as_view(), name='svg_search'),
]

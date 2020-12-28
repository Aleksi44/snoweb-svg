from django.urls import path

from app.views import CollectionList, GroupSvgList, SvgList

app_name = 'app'

urlpatterns = [
    path('', CollectionList.as_view(), name='collection'),
    path('icons/', GroupSvgList.as_view(), name='group'),
    path('icons/<collection_key>/', GroupSvgList.as_view(), name='group'),
    path('svg/', SvgList.as_view(), name='svg'),
    path('svg/<collection_key>/<group_key>/', SvgList.as_view(), name='svg'),
    path('svg/<collection_key>/<group_key>/<svg_key>/', SvgList.as_view(), name='svg'),
]

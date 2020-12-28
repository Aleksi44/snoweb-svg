from django.urls import path

from app.views import CollectionList, GroupSvgList

app_name = 'app'

urlpatterns = [
    path('', CollectionList.as_view(), name='collection'),
    path('icons/', GroupSvgList.as_view(), name='group'),
    path('icons/<collection_key>/', GroupSvgList.as_view(), name='group'),
]

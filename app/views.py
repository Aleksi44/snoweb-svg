from django.views.generic import ListView
from snowebsvg.models import Collection, GroupSvg


class CollectionList(ListView):
    model = Collection
    template_name = 'app/collection_list.html'


class GroupSvgList(ListView):
    model = GroupSvg
    template_name = 'app/groupsvg_list.html'

    def get_queryset(self):
        collection_key = self.kwargs.get('collection_key')
        if collection_key:
            return self.model.objects.filter(collection__key=collection_key)
        return self.model.objects.all()

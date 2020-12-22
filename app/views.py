from django.views.generic import ListView
from snowebsvg.models import Collection, GroupSvg, Svg


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


class SvgList(ListView):
    model = Svg
    template_name = 'app/svg_list.html'

    def get_queryset(self):
        group_key = self.kwargs.get('group_key')
        collection_key = self.kwargs.get('collection_key')
        if group_key and not collection_key:
            return self.model.objects.filter(group__key=group_key)
        if group_key and collection_key:
            return self.model.objects.filter(
                group__key=group_key,
                group__collection__key=collection_key
            )
        return self.model.objects.all()

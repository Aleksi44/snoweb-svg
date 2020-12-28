from django.views.generic import ListView
from snowebsvg.models import Collection, GroupSvg, Svg


class AppMixin(ListView):
    def post(self, request, *args, **kwargs):
        if 'theme' in request.POST:
            request.session['theme'] = request.POST['theme']
        return super().get(request, *args, **kwargs)


class CollectionList(AppMixin):
    model = Collection
    template_name = 'app/collection_list.html'


class GroupSvgList(AppMixin):
    model = GroupSvg
    template_name = 'app/groupsvg_list.html'

    def get_queryset(self):
        collection_key = self.kwargs.get('collection_key')
        if collection_key:
            return self.model.objects.filter(collection__key=collection_key)
        return self.model.objects.all()


class SvgList(AppMixin):
    model = Svg
    template_name = 'app/svg_list.html'

    def get_queryset(self):
        group_key = self.kwargs.get('group_key')
        collection_key = self.kwargs.get('collection_key')
        svg_key = self.kwargs.get('svg_key')
        if group_key and not collection_key and not svg_key:
            return self.model.objects.filter(group__key=group_key)
        if group_key and collection_key and not svg_key:
            return self.model.objects.filter(
                group__key=group_key,
                group__collection__key=collection_key
            )
        if group_key and collection_key and svg_key:
            return self.model.objects.filter(
                group__key=group_key,
                group__collection__key=collection_key,
                key=svg_key
            )
        return self.model.objects.all()

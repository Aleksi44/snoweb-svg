from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import redirect
from django.template.defaultfilters import slugify

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
        svg_key = self.kwargs.get('svg_key')
        if group_key and collection_key and svg_key:
            return self.model.objects.filter(
                group__key=group_key,
                group__collection__key=collection_key,
                key=svg_key
            )
        return self.model.objects.all()


class SvgSearch(ListView):
    model = Svg
    template_name = 'app/svg_search.html'

    def get_queryset(self):
        key = self.kwargs.get('key')
        if key:
            return self.model.objects.filter(
                Q(key__icontains=key) |
                Q(group__key__icontains=key) |
                Q(group__collection__key__icontains=key)
            )
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(SvgSearch, self).get_context_data(**kwargs)
        context['key'] = self.kwargs.get('key')
        return context

    def post(self, request, *args, **kwargs):
        key = request.POST.get('key', None)
        if key:
            key_slug = slugify(key)
            if key_slug:
                return redirect('app:svg_search', key=key_slug)
        return redirect('app:svg_search')

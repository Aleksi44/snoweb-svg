from django.views.generic import ListView, TemplateView
from django.db.models import Q
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.db.models import Count

from snowebsvg.settings import SVG_DEFAULT_VARIANT, SVG_DEFAULT_THEME
from snowebsvg.models import Collection, Svg
from app.forms import \
    ThemeDarkForm, \
    ThemeLightForm, \
    ThemeLightAppForm, \
    ThemeDarkAppForm
from app.templatetags.settings import current_settings

MAX_SVG_RESULTS = 275


class SvgListView(ListView):
    model = Svg
    template_name = 'app/svg_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SvgListView, self).get_context_data(**kwargs)
        context['tag_related'] = Collection.objects.all()
        return context

    def get_queryset(self):
        group_key = self.kwargs.get('group_key')
        collection_key = self.kwargs.get('collection_key')
        svg_key = self.kwargs.get('svg_key')
        if group_key and collection_key and svg_key:
            objects = self.model.objects.filter(
                group__key=group_key,
                group__collection__key=collection_key,
                key=svg_key
            )
            if objects.count() == 0:
                raise Http404
            return objects
        return self.model.objects.all()


class SvgSearchView(TemplateView):
    template_name = 'app/svg_list.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        page = request.GET.get('page', 1)
        paginator = Paginator(context['qs'], MAX_SVG_RESULTS)
        try:
            search_results = paginator.page(page)
        except PageNotAnInteger:
            search_results = paginator.page(1)
        except EmptyPage:
            search_results = paginator.page(paginator.num_pages)
        context['object_list'] = search_results
        return self.render_to_response(context)

    def get_queryset(self):
        key = self.kwargs.get('key')
        if key:
            qs = Svg.objects.filter(
                Q(key__icontains=key) |
                Q(group__key__icontains=key) |
                Q(group__collection__key__icontains=key)
            )
        else:
            qs = Svg.objects.all()
        return qs.order_by('group__key')

    def get_context_data(self, **kwargs):
        context = super(SvgSearchView, self).get_context_data(**kwargs)
        key = self.kwargs.get('key')
        qs = self.get_queryset()
        if key:
            context['key_title'] = key.replace('_', ' ').title()
            # qs_group_key = qs.values('group__key').annotate(Count('group__key')).order_by('-group__key__count')
            # context['tag_related'] = [Svg(key=group_key['group__key']) for group_key in qs_group_key]
        else:
            pass
            # context['tag_related'] = Collection.objects.all()
        context['tag_related'] = Collection.objects.all()
        context['key'] = key
        context['qs'] = qs
        return context

    def post(self, request, *args, **kwargs):
        key = request.POST.get('key', None)
        if key:
            key = key.replace(' ', '_')
            key = key.replace('-', '_')
            key_slug = slugify(key)
            if key_slug:
                return redirect('app:svg_search', key=key_slug)
        return redirect('app:svg_search')


class SvgSettingsView(TemplateView):
    template_name = 'app/svg_settings.html'
    forms = (
        ('form_theme_dark', ThemeDarkForm),
        ('form_theme_light', ThemeLightForm),
        ('form_theme_dark_app', ThemeDarkAppForm),
        ('form_theme_light_app', ThemeLightAppForm),
    )

    def get_context_data(self, request, **kwargs):
        context = {}
        for form_key, form in self.forms:
            context[form_key] = form(current_settings(request))
        context['tag_related'] = Collection.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_key = request.POST.get('form_key', None)
        if form_key and any(tuple_form[0] == form_key for tuple_form in self.forms):
            form = dict(self.forms)[form_key](request.POST)
            if form.is_valid():
                for key, value in form.clean().items():
                    request.session['settings'][key] = value
                request.session.modified = True
            else:
                context = self.get_context_data(request, **kwargs)
                context[form_key] = form
                return render(request, self.template_name, context)
        elif request.POST.get('reset', None) == 'reset':
            request.session['settings'] = {}
            request.session['theme'] = SVG_DEFAULT_THEME
            request.session['variant'] = SVG_DEFAULT_VARIANT
        return render(
            request,
            self.template_name,
            self.get_context_data(request, **kwargs)
        )

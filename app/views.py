from django.views.generic import View, TemplateView
from django.db.models import Q
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.http import HttpResponse
from django.template.loader import get_template
from wand.image import Image
from wand.color import Color
from snowebsvg.settings import SVG_DEFAULT_VARIANT, SVG_DEFAULT_THEME
from snowebsvg.models import Collection, Svg
from app.forms import \
    ThemeDarkForm, \
    ThemeLightForm, \
    ThemeLightAppForm, \
    ThemeDarkAppForm
from app.templatetags.settings import current_settings

MAX_SVG_RESULTS = 275


class SvgDetailMixin:
    kwargs = None

    def get_queryset(self):
        group_key = self.kwargs.get('group_key')
        collection_key = self.kwargs.get('collection_key')
        svg_key = self.kwargs.get('svg_key')
        if group_key and collection_key and svg_key:
            objects = Svg.objects.filter(
                group__key=group_key,
                group__collection__key=collection_key,
                key=svg_key
            )
            if objects.count() == 1:
                return objects.first()
        raise Http404


class SvgDetailView(TemplateView, SvgDetailMixin):
    template_name = 'app/svg_detail.html'
    forms = (
        ('form_theme_dark', ThemeDarkForm),
        ('form_theme_light', ThemeLightForm),
        ('form_theme_dark_app', ThemeDarkAppForm),
        ('form_theme_light_app', ThemeLightAppForm),
    )

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

    def get_context_data(self, request, **kwargs):
        context = {}
        for form_key, form in self.forms:
            context[form_key] = form(current_settings(request))
        context['collections'] = Collection.objects.all()
        svg = self.get_queryset()
        context['svg'] = svg
        context['svg_related'] = Svg.objects.filter(group__key=svg.group.key).exclude(key=svg.key)

        # Tmp monkey patch / replace with real search engine
        clean_svg_key = svg.key.replace('_1', '')
        clean_svg_key = clean_svg_key.replace('_2', '')
        clean_svg_key = clean_svg_key.replace('_3', '')
        clean_svg_key = clean_svg_key.replace('_4', '')

        group_related = Svg.objects.filter(group__collection__key=svg.group.collection.key,
                                           key__contains=clean_svg_key).exclude(
            group__collection__key=svg.group.collection.key,
            group__key=svg.group.key,
        )
        if group_related.count() == 0:
            context['group_related'] = Svg.objects.filter(group__collection__key=svg.group.collection.key).exclude(
                group__collection__key=svg.group.collection.key,
                group__key=svg.group.key,
            )
        else:
            context['group_related'] = group_related
        return context


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
        context['collections'] = Collection.objects.all()
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


class SvgDownloadView(View, SvgDetailMixin):
    def post(self, request, *args, **kwargs):
        svg = self.get_queryset()
        template = get_template(svg.path_entry)
        theme = request.session.get('theme', SVG_DEFAULT_THEME)
        content_svg = template.render({
            'self': svg,
            'theme': theme,
            'width': '100%',
            'height': '100%',
            'grid': False,
            'variant': request.session.get('variant', SVG_DEFAULT_VARIANT),
            'css': True,
            'request': request
        })
        extension = request.POST.get('extension', 'svg')
        filename = svg.key_composer + '.' + extension
        if extension == 'png':
            session_settings = request.session.get('settings', {})
            background = session_settings.get(f'theme_{theme}_background_body', '#FFF')
            with Image(blob=content_svg.encode(), format='svg', background=background) as img:
                response = HttpResponse(img.make_blob(format='png'), content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
                return response
        elif extension == 'svg':
            response = HttpResponse(content_svg, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
            return response

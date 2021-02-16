import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from django.utils.functional import cached_property
from django.template.loaders.app_directories import Loader
from django.template.exceptions import TemplateDoesNotExist
from wagtail.search import index
from snowebsvg import settings


class Collection(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("Key"))

    class Meta:
        ordering = ('key',)

    def __str__(self):
        return self.key.title()

    @cached_property
    def root_directory(self):
        for template_directory in Loader('django').get_dirs():
            template_directory = str(template_directory)
            if '/snowebsvg/' in template_directory:
                base_dir_svg = "%s/snowebsvg" % template_directory
                return "%s/%s" % (
                    base_dir_svg,
                    'collections'
                )

    def build(self):
        """
        Build all collection group's available in django apps template folder named :
        ``snowebsvg/collections/<collection_key>``
        """
        conf_files = [
            'django.html',
            'styles.html',
            '_preview.html',
        ]
        for group_key in os.listdir("%s/%s" % (self.root_directory, self.key)):
            if group_key not in conf_files:
                group, _ = GroupSvg.objects.get_or_create(key=group_key, collection_id=self.id)
                group.build()

    def render_styles(self):
        """
        Method for rendering stylesheet code
        """

        context = {
            'self': self,
            'settings': settings
        }
        try:
            svg_template = get_template("snowebsvg/collections/%s/styles.html" % self.key)
            return svg_template.render(context)
        except TemplateDoesNotExist:
            svg_template = get_template("snowebsvg/common/styles.html")
            return svg_template.render(context)


class GroupSvg(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("Key"))
    collection = models.ForeignKey(
        Collection,
        default=None,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        ordering = ('key',)

    def __str__(self):
        return self.key.title()

    @cached_property
    def path_entry(self):
        """
        File path of a ``GroupSvg``
        """
        return "%s/%s/%s" % (
            self.collection.root_directory,
            self.collection.key,
            self.key
        )

    def build(self):
        """
        Build all ``Svg`` available in django apps template folder named :
        ``snowebsvg/collections/<collection_key>/<group_svg_key>``
        """
        try:
            for html_filename in os.listdir(self.path_entry):
                svg_key = html_filename.replace('.html', '')
                # We don't build private files
                if not svg_key.startswith('_'):
                    try:
                        Svg.objects.get(
                            key=svg_key,
                            group_id=self.id
                        )
                    except Svg.DoesNotExist:
                        svg = Svg(
                            key=svg_key,
                            group_id=self.id
                        )
                        svg.save()
        except NotADirectoryError:
            # `self.path_entry` is not a directory, pass it
            pass


class Svg(index.Indexed, models.Model):
    key = models.CharField(max_length=255, verbose_name=_("Key"))
    group = models.ForeignKey(
        GroupSvg,
        default=None,
        on_delete=models.CASCADE,
        null=True
    )

    # Wagtail index
    search_fields = [
        index.SearchField('key_composer', partial_match=True),
    ]

    class Meta:
        ordering = ('key',)

    def __str__(self):
        return self.key_composer.title().replace('-', ' ').replace('_', ' ')

    @cached_property
    def path_entry(self):
        """
        :return string: Path html of Svg
        """
        return "snowebsvg/collections/%s/%s/%s.html" % (
            self.group.collection.key,
            self.group.key,
            self.key
        )

    @cached_property
    def key_composer(self):
        """
        :return string: Unique Identifier of Svg
        """
        return "%s-%s-%s" % (
            self.group.collection.key,
            self.group.key,
            self.key
        )

    def key_decomposer(self, key_composer):
        """
        :return svg: Svg instance by key composer
        """
        collection_key, group_key, key = key_composer.split('-')
        return Svg.objects.get(
            key=key,
            group__key=group_key,
            group__collection__key=collection_key
        )

    def render_django(self, theme=settings.SVG_DEFAULT_THEME, width=settings.SVG_DEFAULT_WIDTH,
                      height=settings.SVG_DEFAULT_HEIGHT, variant=settings.SVG_DEFAULT_VARIANT):
        """
        Method for rendering Django template code

        :param theme: Theme, defaults to :ref:`SVG_DEFAULT_THEME <references_settings>`
        :param width: Width, defaults :ref:`SVG_DEFAULT_WIDTH <references_settings>`
        :param height: Height, defaults :ref:`SVG_DEFAULT_HEIGHT <references_settings>`
        :param variant: Variant, defaults :ref:`SVG_DEFAULT_VARIANT <references_settings>`
        """
        context = {
            'self': self,
            'theme': theme,
            'width': width,
            'height': height,
            'variant': variant,
            'start': '{%',
            'end': '%}'
        }
        try:
            svg_template = get_template("snowebsvg/collections/%s/%s/_django.html" % (
                self.group.collection.key,
                self.group.key,
            ))
            return svg_template.render(context)
        except TemplateDoesNotExist:
            svg_template = get_template("snowebsvg/common/django.html")
            return svg_template.render(context)

    def render_html(self, theme=settings.SVG_DEFAULT_THEME, width=settings.SVG_DEFAULT_WIDTH,
                    height=settings.SVG_DEFAULT_HEIGHT, variant=settings.SVG_DEFAULT_VARIANT,
                    grid=False, klass=None):
        """
        Method for rendering Svg to HTML

        :param theme: Theme, defaults to :ref:`SVG_DEFAULT_THEME <references_settings>`
        :param width: Width, defaults :ref:`SVG_DEFAULT_WIDTH <references_settings>`
        :param height: Height, defaults :ref:`SVG_DEFAULT_HEIGHT <references_settings>`
        :param grid: Grid, add grid for debugging SVG, defaults to False`
        :param variant: Variant, defaults :ref:`SVG_DEFAULT_VARIANT <references_settings>`
        :param klass: extra css class
        """
        svg_template = get_template(self.path_entry)
        return svg_template.render({
            'self': self,
            'theme': theme,
            'width': width,
            'height': height,
            'grid': grid,
            'variant': variant,
            'klass': klass
        })

    def render_preview(self, theme=settings.SVG_DEFAULT_THEME, width=settings.SVG_DEFAULT_WIDTH,
                       height=settings.SVG_DEFAULT_HEIGHT, variant=settings.SVG_DEFAULT_VARIANT, grid=False):
        """
        Method for rendering a preview of Svg to HTML

        If _preview.html exist, then render the preview html file.
        If _preview.html does not exist, then fall back to the common preview.html file.

        :param theme: Theme, defaults to :ref:`SVG_DEFAULT_THEME <references_settings>`
        :param width: Width, defaults :ref:`SVG_DEFAULT_WIDTH <references_settings>`
        :param height: Height, defaults :ref:`SVG_DEFAULT_HEIGHT <references_settings>`
        :param grid: Grid, add grid for debugging SVG, defaults to False`
        :param variant: Variant, defaults :ref:`SVG_DEFAULT_VARIANT <references_settings>`

        """
        context = {
            'self': self,
            'theme': theme,
            'width': width,
            'height': height,
            'grid': grid,
            'variant': variant
        }
        try:
            svg_template = get_template("snowebsvg/collections/%s/%s/_preview.html" % (
                self.group.collection.key,
                self.group.key,
            ))
            return svg_template.render(context)
        except TemplateDoesNotExist:
            svg_template = get_template("snowebsvg/common/preview.html")
            return svg_template.render(context)

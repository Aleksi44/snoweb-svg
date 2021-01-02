import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from django.utils.functional import cached_property
from django.template.loaders.app_directories import Loader

from snowebsvg import settings


class Collection(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("key"))

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
        Build all collections available in django apps template folder named :
        ``snowebsvg/collections``
        """
        for group_key in os.listdir("%s/%s" % (self.root_directory, self.key)):
            group, _ = GroupSvg.objects.get_or_create(key=group_key, collection_id=self.id)
            group.build()

    def render_styles(self, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE):
        """
        Method for rendering stylesheet and styles code
        """
        svg_template = get_template("snowebsvg/common/collection_render_styles.html")
        return svg_template.render({
            'self': self,
            'theme': theme,
            'size': size,
            'settings': settings
        })


class GroupSvg(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("key"))
    collection = models.ForeignKey(
        Collection,
        default=None,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.key.title()

    @cached_property
    def key_composer(self):
        """
        Unique key Identifier of ``GroupSvg``
        """
        return "%s-%s" % (
            self.collection.key,
            self.key
        )

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


class Svg(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("key"))
    group = models.ForeignKey(
        GroupSvg,
        default=None,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.key.title()

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

    def render_django(self, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE):
        """
        Method for rendering Django template code
        """
        svg_template = get_template("snowebsvg/common/svg_render_django.html")
        return svg_template.render({
            'self': self,
            'theme': theme,
            'size': size,
            'start': '{%',
            'end': '%}'
        })

    def render_html(self, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE):
        """
        Method for rendering Svg to HTML

        :param theme: Theme, defaults to :ref:`SVG_DEFAULT_THEME <references_settings>`
        :param size: Size, defaults :ref:`SVG_DEFAULT_SIZE <references_settings>`
        """
        svg_template = get_template("snowebsvg/collections/%s/%s/%s" % (
            self.group.collection.key,
            self.group.key,
            self.key + '.html'
        ))
        return svg_template.render({
            'self': self,
            'theme': theme,
            'size': size
        })

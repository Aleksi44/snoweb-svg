from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from django.utils.functional import cached_property
from django.template.exceptions import TemplateDoesNotExist

from snowebsvg.models import GroupSvg
from snowebsvg import settings


class AbstractSvg(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("Key"))
    group = models.ForeignKey(
        GroupSvg,
        default=None,
        on_delete=models.CASCADE,
        null=True,
        related_name='svg_set'
    )

    class Meta:
        ordering = ('key',)
        abstract = True

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
        from snowebsvg.models import Svg
        collection_key, group_key, key = key_composer.split('-')
        return Svg.objects.get(
            key=key,
            group__key=group_key,
            group__collection__key=collection_key
        )

    def render_django(self, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE,
                      variant=settings.SVG_DEFAULT_VARIANT):
        """
        Method for rendering Django template code

        :param theme: Theme, defaults to :ref:`SVG_DEFAULT_THEME <references_settings>`
        :param size: Size, defaults :ref:`SVG_DEFAULT_SIZE <references_settings>`
        :param variant: Variant, defaults :ref:`SVG_DEFAULT_VARIANT <references_settings>`
        """
        context = {
            'self': self,
            'theme': theme,
            'size': size,
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

    def render_html(self, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE,
                    variant=settings.SVG_DEFAULT_VARIANT, grid=False, klass=None):
        """
        Method for rendering Svg to HTML

        :param theme: Theme, defaults to :ref:`SVG_DEFAULT_THEME <references_settings>`
        :param size: Size, defaults :ref:`SVG_DEFAULT_SIZE <references_settings>`
        :param grid: Grid, add grid for debugging SVG, defaults to False`
        :param variant: Variant, defaults :ref:`SVG_DEFAULT_VARIANT <references_settings>`
        :param klass: extra css class
        """
        svg_template = get_template(self.path_entry)
        return svg_template.render({
            'self': self,
            'theme': theme,
            'size': size,
            'grid': grid,
            'variant': variant,
            'klass': klass
        })

    def render_preview(self, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE,
                       variant=settings.SVG_DEFAULT_VARIANT, grid=False):
        """
        Method for rendering a preview of Svg to HTML

        If _preview.html exist, then render the preview html file.
        If _preview.html does not exist, then fall back to the common preview.html file.

        :param theme: Theme, defaults to :ref:`SVG_DEFAULT_THEME <references_settings>`
        :param size: Size, defaults :ref:`SVG_DEFAULT_SIZE <references_settings>`
        :param grid: Grid, add grid for debugging SVG, defaults to False`
        :param variant: Variant, defaults :ref:`SVG_DEFAULT_VARIANT <references_settings>`

        """
        context = {
            'self': self,
            'theme': theme,
            'size': size,
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

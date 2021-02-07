import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from django.utils.functional import cached_property
from django.template.loaders.app_directories import Loader

from snowebsvg import settings
from snowebsvg import loader


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

    def render_styles(self, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE):
        """
        Method for rendering stylesheet code
        """
        svg_template = get_template("snowebsvg/collections/%s/styles.html" % self.key)
        return svg_template.render({
            'self': self,
            'theme': theme,
            'size': size,
            'settings': settings
        })


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


if loader.SVG_MODEL == loader.DEFAULT_SVG_MODEL:
    from snowebsvg.abstract import AbstractSvg


    class DefaultSvg(AbstractSvg):
        pass

Svg = loader.import_from_string(loader.SVG_MODEL)

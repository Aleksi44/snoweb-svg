import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from snowebsvg import settings


class Collection(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("name"))

    def __str__(self):
        return self.key.title()

    def build(self):
        """
        Build all collections available in django apps template folder named :
        ``snowebsvg/collections``
        """
        for group_key in os.listdir("%s/%s" % (settings.dir_collection(), self.key)):
            group, _ = GroupSvg.objects.get_or_create(key=group_key, collection_id=self.id)
            group.build()


class GroupSvg(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("key"), help_text='dfgdfg')
    collection = models.ForeignKey(
        Collection,
        default=None,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.key.title()

    @property
    def path(self):
        """
        Unique Identifier of ``GroupSvg``
        """
        return "%s-%s" % (
            self.collection.key,
            self.key
        )

    @property
    def path_svg(self):
        """
        File path of a ``GroupSvg``
        """
        return "%s/%s/%s" % (
            settings.dir_collection(),
            self.collection.key,
            self.key
        )

    def build(self):
        """
        Build all ``Svg`` available in django apps template folder named :
        ``snowebsvg/collections/<collection_key>/<group_svg_key>``
        """
        for html_filename in os.listdir(self.path_svg):
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
    key = models.CharField(max_length=255, verbose_name=_("title"))
    group = models.ForeignKey(
        GroupSvg,
        default=None,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.key.title()

    @property
    def path(self):
        """
        Unique Identifier of Svg
        """
        return "%s-%s-%s" % (
            self.group.collection.key,
            self.group.key,
            self.key
        )

    def render(self, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE):
        """
        Method for rendering an Svg

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

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
        for group_key in os.listdir("%s/%s" % (settings.BASE_DIR_COLLECTION, self.key)):
            group, _ = GroupSvg.objects.get_or_create(key=group_key, collection_id=self.id)
            group.build()


class GroupSvg(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("key"))
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
        return "%s-%s" % (
            self.collection.key,
            self.key
        )

    @property
    def path_svg(self):
        return "%s/%s/%s" % (
            settings.BASE_DIR_COLLECTION,
            self.collection.key,
            self.key
        )

    def build(self):
        for html_filename in os.listdir(self.path_svg):
            svg_key = html_filename.replace('.html', '')
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
        return "%s-%s-%s" % (
            self.group.collection.key,
            self.group.key,
            self.key
        )

    def render(self, theme=settings.SVG_DEFAULT_THEME, size=settings.SVG_DEFAULT_SIZE):
        svg_template = get_template("%s/%s" % (
            self.group.path_svg,
            self.key + '.html'
        ))
        return svg_template.render({
            'self': self,
            'theme': theme,
            'size': size
        })

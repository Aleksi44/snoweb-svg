from pathlib import Path
from django.db import models
from django.utils.translation import gettext_lazy as _
from snowebsvg import settings

from django.template.loader import get_template
from django.core.files.images import ImageFile
import os


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
        return "%s:%s" % (
            self.collection.key,
            self.key
        )

    @property
    def path_build(self):
        return "%s/%s/%s" % (
            settings.BASE_DIR_SVG_BUILD,
            self.collection.key,
            self.key
        )

    def build(self):
        events = []
        svg_path = "%s/%s/%s" % (
            settings.BASE_DIR_COLLECTION,
            self.collection.key,
            self.key
        )
        Path(self.path_build).mkdir(parents=True, exist_ok=True)

        for event_html_filename in os.listdir(svg_path):
            event = event_html_filename.replace('.html', '')
            event_tpl = get_template("%s/%s" % (svg_path, event_html_filename))
            events.append({
                'id': "event-%s-%s-%s" % (
                    self.collection.key,
                    self.key,
                    event
                ),
                'render': event_tpl.render()
            })
        svg_template = get_template('snowebsvg/svg/square_100.html')
        svg_content = svg_template.render({'events': events})

        path_build_file = "%s/group.svg" % self.path_build
        svg_file_build = open(path_build_file, "a")
        svg_file_build.truncate(0)
        svg_file_build.write(svg_content)
        svg_file_build.close()

        svg_file_image = ImageFile(
            open(path_build_file, "rb"),
            name=self.key
        )

        try:
            Svg.objects.get(
                key=self.key,
                group_id=self.id
            )
        except Svg.DoesNotExist:
            svg = Svg(
                key=self.key,
                file=svg_file_image,
                group_id=self.id
            )
            svg.save()


class Svg(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("title"))
    file = models.FileField(upload_to="media", verbose_name=_("file"))
    group = models.ForeignKey(
        GroupSvg,
        default=None,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.key.title()

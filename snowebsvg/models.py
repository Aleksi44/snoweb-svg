from django.db import models
from django.utils.translation import gettext_lazy as _


class Collection(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("name"))

    def __str__(self):
        return self.key.title()


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

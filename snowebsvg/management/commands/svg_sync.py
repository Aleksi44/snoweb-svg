import os
from django.core.management.base import BaseCommand
from snowebsvg.models import Collection, GroupSvg, Svg


class Command(BaseCommand):

    def handle(self, *args, **options):
        for collection in Collection.objects.all():
            collection_path = "%s/%s" % (collection.root_directory, collection.key)
            if not os.path.isdir(collection_path):
                collection.delete()

        for group_svg in GroupSvg.objects.all():
            if not os.path.isdir(group_svg.path_entry):
                group_svg.delete()

        for svg in Svg.objects.all():
            svg_path = "%s/%s.html" % (svg.group.path_entry, svg.key)
            if not os.path.isfile(svg_path):
                svg.delete()

import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile

from snowebsvg.models import Svg, GroupSvg, Collection
from snowebsvg import settings

class Command(BaseCommand):

    def handle(self, *args, **options):
        from django.template.loaders.app_directories import Loader
        from django.template.loader import get_template

        for template_directory in Loader('django').get_dirs():
            template_directory = str(template_directory)

            # TODO: improve `svg` directory detection

            if '/snowebsvg/' in template_directory:
                base_directory = "%s/snowebsvg/%s" % (
                    template_directory,
                    'svg'
                )
                collection_directory = "%s/%s" % (
                    base_directory,
                    'collections'
                )
                for collection_name in os.listdir(collection_directory):
                    print("Collection : %s" % collection_name)
                    collection, _ = Collection.objects.get_or_create(key=collection_name)
                    for icon_key in os.listdir("%s/%s" % (collection_directory, collection_name)):
                        group, _ = GroupSvg.objects.get_or_create(key=icon_key, collection_id=collection.id)
                        print("Icon : %s" % icon_key)
                        svg_path_build = "%s/%s/%s/%s" % (
                            base_directory,
                            'build',
                            collection_name,
                            icon_key
                        )
                        for svg_filename in os.listdir("%s/%s/%s" % (collection_directory, collection_name, icon_key)):
                            svg_key = svg_filename.replace('.svg', '')
                            svg_path_build_file = "%s/%s" % (
                                svg_path_build,
                                svg_filename
                            )
                            Path(svg_path_build).mkdir(parents=True, exist_ok=True)

                            svg_template = get_template('snowebsvg/svg/html.html')
                            svg_content = svg_template.render({
                                'svg_path': 'snowebsvg/svg/collections/%s/%s/%s' % (
                                    collection_name,
                                    icon_key,
                                    svg_filename
                                ),
                            })

                            svg_file_build = open(svg_path_build_file, "a")
                            svg_file_build.truncate(0)
                            svg_file_build.write(svg_content)
                            svg_file_build.close()

                            svg_file_image = ImageFile(
                                open(svg_path_build_file, "rb"),
                                name=svg_key
                            )

                            try:
                                Svg.objects.get(
                                    key=svg_key,
                                    group_id=group.id
                                )
                            except Svg.DoesNotExist:
                                svg = Svg(
                                    key=svg_key,
                                    file=svg_file_image,
                                    group_id=group.id
                                )
                                svg.save()
                            print("SVG : %s" % svg_filename)

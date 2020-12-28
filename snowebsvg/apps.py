from django.apps import AppConfig
from django.template.loaders.app_directories import Loader
from snowebsvg import settings


class SnowebSvgConfig(AppConfig):
    name = 'snowebsvg'
    verbose_name = "Snoweb SVG"

    def ready(self):
        for template_directory in Loader('django').get_dirs():
            template_directory = str(template_directory)
            if '/snowebsvg/' in template_directory:
                base_dir_svg = "%s/snowebsvg" % template_directory
                setattr(settings, 'BASE_DIR_SVG', base_dir_svg)

                collection = "%s/%s" % (
                    base_dir_svg,
                    'collections'
                )
                setattr(settings, 'BASE_DIR_COLLECTION', collection)

                build = "%s/%s" % (
                    base_dir_svg,
                    'build',
                )
                setattr(settings, 'BASE_DIR_SVG_BUILD', build)

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
                svg = "%s/snowebsvg/%s" % (
                    template_directory,
                    'svg'
                )
                setattr(settings, 'BASE_DIR_SVG', svg)

                collection = "%s/%s" % (
                    svg,
                    'collections'
                )
                setattr(settings, 'BASE_DIR_COLLECTION', collection)

                build = "%s/%s" % (
                    svg,
                    'build',
                )
                setattr(settings, 'BASE_DIR_SVG_BUILD', build)

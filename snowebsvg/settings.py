import os
import json
import pkg_resources

BASE_DIR = os.environ['BASE_DIR']

try:
    #  Production part
    VERSION = pkg_resources.get_distribution("snowebsvg").version
except pkg_resources.DistributionNotFound:
    #  Develop part
    with open(os.path.join(BASE_DIR, 'package.json')) as package:
        data = json.load(package)
        VERSION = data['version']

SVG_DEFAULT_THEME = 'dark'
SVG_DEFAULT_SIZE = 'x3'


def build_dir_collection():
    from django.template.loaders.app_directories import Loader
    for template_directory in Loader('django').get_dirs():
        template_directory = str(template_directory)
        if '/snowebsvg/' in template_directory:
            base_dir_svg = "%s/snowebsvg" % template_directory
            return "%s/%s" % (
                base_dir_svg,
                'collections'
            )

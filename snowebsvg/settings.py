import os
import json
import pkg_resources

BASE_URL_CSS = "https://static.snoweb.fr/snowebsvg/dist/css/"

try:
    #  Production part
    VERSION = pkg_resources.get_distribution("snowebsvg").version
except pkg_resources.DistributionNotFound:
    #  Develop part
    BASE_DIR = os.environ['BASE_DIR']
    with open(os.path.join(BASE_DIR, 'package.json')) as package:
        data = json.load(package)
        VERSION = data['version']

SVG_DEFAULT_THEME = 'dark'
SVG_DEFAULT_WIDTH = 100
SVG_DEFAULT_HEIGHT = 100
SVG_DEFAULT_VARIANT = 'glass'

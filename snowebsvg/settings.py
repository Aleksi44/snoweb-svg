import os
import json
import pkg_resources

BASE_URL_CSS = "https://static.snoweb.io/snowebsvg/dist/css/"

try:
    #  Production part
    VERSION = pkg_resources.get_distribution("snowebsvg").version
except pkg_resources.DistributionNotFound:
    #  Develop part
    BASE_DIR = os.environ['BASE_DIR']
    with open(os.path.join(BASE_DIR, 'package.json')) as package:
        data = json.load(package)
        VERSION = data['version']

SVG_DEFAULT_THEME = 'light'
SVG_DEFAULT_WIDTH = 100
SVG_DEFAULT_HEIGHT = 100
SVG_DEFAULT_VARIANT = None
SVG_DEFAULT_KEY = 'decorator-rect-basic'

try:
    import wagtail
    WAGTAIL_INSTALL = True
except ImportError:
    WAGTAIL_INSTALL = False

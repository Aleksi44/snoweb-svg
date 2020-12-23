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

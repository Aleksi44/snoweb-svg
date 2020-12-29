from django.test import TestCase
from django.core import management


class SnowebSvgTest(TestCase):

    def test_build(self):
        management.call_command('svg_build')

import logging
from django.test import TestCase
from django.core import management

from snowebsvg.models import Svg, Collection
from snowebsvg import settings
from snowebsvg.templatetags.svg import \
    svg_inline, \
    svg_django, \
    collection_styles, \
    svg_preview, \
    svg_stylesheets

logger = logging.getLogger('snowebsvg')


class SnowebSvgTest(TestCase):

    def test_svg_build(self):
        management.call_command('svg_build')

    def test_templatetags_svg_inline(self):
        self.test_svg_build()
        for svg in Svg.objects.all():
            logger.debug("svg_inline svg=`%s`" % str(svg))
            logger.debug("svg_inline group_svg=`%s`" % str(svg.group))
            svg_inline(svg)
            svg_inline(svg, variant='glass')
        for svg in Svg.objects.all():
            logger.debug("svg_inline key_composer=`%s`" % str(svg.key_composer))
            svg_inline(svg.key_composer)

    def test_templatetags_svg_django(self):
        self.test_svg_build()
        for svg in Svg.objects.all():
            logger.debug("svg_django svg=`%s`" % str(svg))
            svg_django(svg)
        for svg in Svg.objects.all():
            logger.debug("svg_django key_composer=`%s`" % str(svg.key_composer))
            svg_django(svg.key_composer)

    def test_templatetags_svg_preview(self):
        self.test_svg_build()
        for svg in Svg.objects.all():
            logger.debug("svg_preview svg=`%s`" % str(svg))
            svg_preview(svg)
        for svg in Svg.objects.all():
            logger.debug("svg_preview key_composer=`%s`" % str(svg.key_composer))
            svg_preview(svg.key_composer)

    def test_templatetags_collection_styles(self):
        self.test_svg_build()
        for collection in Collection.objects.all():
            logger.debug("collection_styles collection=`%s`" % str(collection))
            collection_styles(collection)

    def test_variant_manager(self):
        self.test_svg_build()

    def test_svg_stylesheets(self):
        bundles = svg_stylesheets('themes')
        self.assertEqual(
            bundles,
            """<link rel="stylesheet" href="%sthemes-%s.css">""" % (
                settings.BASE_URL_CSS,
                settings.VERSION
            )
        )

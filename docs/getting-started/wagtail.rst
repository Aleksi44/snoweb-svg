.. _getting-started_wagtail:

Integration with Wagtail
========================

Wagtail integration is the same as Django, you need to follow these guides :

- :doc:`Setup with Django <django>`
- :doc:`Add CSS files with Django <django>`

Here are the additional steps to be able to add Snoweb SVG in a Wagtail block.

1 - Register snippet
--------------------

Add the code below to register the SVG model in the wagtail snippets :

::

    from wagtail.snippets.models import register_snippet
    from snowebsvg.models import Svg

    register_snippet(Svg)

2 - Create a chooser block
--------------------------

Here is an example of a chooser block to be able to choose an SVG from the Wagtail CMS :

::

    from wagtail.snippets.blocks import SnippetChooserBlock
    from snowebsvg.models import Svg


    class SnowebSvgChooserBlock(SnippetChooserBlock):
        def __init__(self, target_model=Svg, **kwargs):
            super().__init__(target_model, **kwargs)
            self._target_model = target_model

        class Meta:
            icon = 'image'
            max_num = 1


Now, you can include ``SnowebSvgChooserBlock`` like :

::

    class DrawerBlock(blocks.StructBlock):
        svg = SnowebSvgChooserBlock()


3 - Render SVG with Wagtail block template
------------------------------------------

You can use ``svg_inline`` to include an SVG in your Wagtail block template with these parameters :

- ``svg`` : instance of ``SnowebSvgChooserBlock``.
- ``<theme>`` : ``'light'`` or ``'dark'``, see more at :doc:`Themes <../references/css>`.
- ``<width>`` : ``100``, ``100%``, ``auto``, see more at `SVG width <https://developer.mozilla.org/fr/docs/Web/SVG/Attribute/width>`_.
- ``<height>`` : ``100``, ``100%``, ``auto``, see more at `SVG height <https://developer.mozilla.org/fr/docs/Web/SVG/Attribute/height>`_.
- ``<variant>`` : ``'none'`` or ``'glass'``, see more at :doc:`Variant <../references/settings>`.
- ``<grid>`` : ``True`` or ``False``, display a grid preview.
- ``<klass>`` : Add extra css classes to <svg> element.


::

    {% load svg %}

    <a href="#" class="svg-trigger">
        {% svg_inline value.svg '<theme>' '<width>' '<height>' '<variant>' '<grid>' '<klass>' %}
    </a>

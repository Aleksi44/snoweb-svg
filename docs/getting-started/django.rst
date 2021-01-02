.. _getting-started_django:

Integration with Django
=======================


Setup
-----

1 - Install with pip :

``pip install snowebsvg``

2 - Add ``snowebsvg`` to django apps installed :

::

    INSTALLED_APPS = [
        ...
        'snowebsvg',
    ]

3 - Run migrations :

``python manage.py migrate``

4 - Build SVG :

``python manage.py svg_build``

Add CSS Files
-------------

You need to :doc:`add css files <html>`.


Add SVG Content
---------------

With :

- ``<svg_key>`` : choose at `svg.snoweb.fr <https://svg.snoweb.fr>`_.
- ``<theme>`` : light or dark, see more :doc:`here <../references/css>`.
- ``<size>`` : x1, x2, ect... see more :doc:`here <../references/css>`.

::

    {% load svg %}

    <a href="#" class="svg-trigger">
        {% svg_inline '<svg_key>' '<theme>' '<size>' %}
    </a>

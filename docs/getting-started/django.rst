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

WIP

::

    {% load svg %}

    <a href="#" class="svg-trigger">
        {% svg_inline 'essential-back-basic' 'dark' 'x3' %}
    </a>

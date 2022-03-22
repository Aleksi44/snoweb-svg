.. _getting-started_django:

Integration with Django
=======================


1 - Setup
---------

1 - Install with pip

::

    pip install snowebsvg


2 - Add ``snowebsvg`` to django apps installed :

::

    INSTALLED_APPS = [
        ...
        'snowebsvg',
    ]

3 - Run migrations

::

    python manage.py migrate

4 - Build SVG

::

    python manage.py svg_build

Now, you have the list of available svg in your database.

2 - Add CSS files
-----------------

There are 2 different methods to configure CSS files with Django :

- You can add css files like the :doc:`HTML getting started <html>`.

- Or you can use django templatetags as below :

::

    {% load svg %}

    ...

    <head>

        ...

        {% autoescape off %}
            {% svg_stylesheets 'themes' 'core' %}
        {% endautoescape %}
    </head>


The version of css files is determined based on the pypi package installed.

You also need to configure :doc:`colors <html>` and :doc:`animations <html>` as needed.

3 - Add SVG in your Django HTML template
----------------------------------------

You can use ``svg_inline`` to include an SVG in your template with these parameters :

- ``<svg_key>`` : choose at `Snoweb SVG <https://www.snoweb-svg.com/svg/>`_.
- ``<theme>`` : ``'light'`` or ``'dark'``, see more :doc:`here <../references/css>`.
- ``<width>`` : ``100``, ``100%``, ``auto``, see more at `SVG width <https://developer.mozilla.org/fr/docs/Web/SVG/Attribute/width>`_.
- ``<height>`` : ``100``, ``100%``, ``auto``, see more at `SVG height <https://developer.mozilla.org/fr/docs/Web/SVG/Attribute/height>`_.
- ``<variant>`` : ``'none'`` or ``'glass'``, see more :doc:`here <../references/settings>`.
- ``<grid>`` : ``True`` or ``False``, display a grid preview.
- ``<klass>`` : Add extra css classes to <svg> element.


::

    {% load svg %}

    <a href="#" class="svg-trigger">
        {% svg_inline '<svg_key>' '<theme>' '<width>' '<height>' '<variant>' '<grid>' '<klass>' %}
    </a>

.. _getting-started_html:


Integration with HTML
=====================


Add CSS Files
-------------

With :

- <version> :

.. image:: https://img.shields.io/pypi/v/snowebsvg
    :target: https://pypi.org/project/snowebsvg/

- <collection_key> :

Choose at `svg.snoweb.fr <https://svg.snoweb.fr>`_.

::

    <head>

        ...

        <!--Themes : manage dark and light mode-->
        <link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/themes-<version>.css">
        <!--Sizer : add default size to SVGs-->
        <link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/themes-<version>.css">

        <!--Add your Snoweb SVG collections CSS like this-->
        <link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/<collection_key>-<version>.css">

        <!--Configure vars-->
        <style>
            :root {
                --svg-theme-light-primary: #14253A;
                --svg-theme-light-secondary: #E63946;
                --svg-theme-dark-primary: #F7F7F7;
                --svg-theme-dark-secondary: #E63946;
            }
        </style>
    </head>


Add SVG Content
---------------

Choose and add your SVG content in your html at `svg.snoweb.fr <https://svg.snoweb.fr>`_.

.. _getting-started_html:


Integration with HTML
=====================


Add CSS Files
-------------

With :

- <version> : current version is |version|

.. image:: https://img.shields.io/pypi/v/snowebsvg
    :target: https://pypi.org/project/snowebsvg/

- <collection_key> : Choose at `svg.snoweb.fr <https://svg.snoweb.fr>`_.

::

    <head>

        ...

        <!--Themes (not required) : manage dark and light mode-->
        <link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/themes-<version>.css">
        <!--Sizer (not required) : add default size to SVGs-->
        <link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/sizer-<version>.css">

        <!--Add your Snoweb SVG collections CSS like this-->
        <link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/<collection_key>-<version>.css">

        <!--Configure colors-->
        <style>
            :root {
                --svg-theme-light-primary: #14253A;
                --svg-theme-light-secondary: #E63946;
                --svg-theme-light-tertiary: #f7f7f7;

                --svg-theme-dark-primary: #F7F7F7;
                --svg-theme-dark-secondary: #E63946;
                --svg-theme-dark-tertiary: #112032;
            }
        </style>
    </head>


Add SVG Content
---------------

Choose and add your SVG content in your html at `svg.snoweb.fr <https://svg.snoweb.fr>`_.

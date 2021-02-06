.. _getting-started_html:


Integration with HTML
=====================


Add CSS Files
-------------

With :

- <version> : current version is |version|

.. image:: https://img.shields.io/pypi/v/snowebsvg
    :target: https://pypi.org/project/snowebsvg/


::

    <head>

        ...

        <!--Themes (not required) : manage dark and light mode with class-->
        <link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/themes-<version>.css">

        <!--Themes auto (not required) : manage dark and light mode with prefers-color-scheme-->
        <link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/themesauto-<version>.css">

        <!--Sizer (not required) : add default size to SVGs-->
        <link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/sizer-<version>.css">

        <!--Effect (not required) : freeze animation for some collections -->
        <link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/effect-<version>.css">

        <!--Builders (required for some collections) : add animations builders -->
        <link rel="stylesheet" href="https://static.snoweb.fr/snowebsvg/dist/css/essential-<version>.css">

        <!--Configure colors (not required if you don't use theme) -->
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

Choose and add your SVG content in your html at `www.snoweb-svg.com <https://www.snoweb-svg.com/en/>`_.

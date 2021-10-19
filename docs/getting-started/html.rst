.. _getting-started_html:


Integration with HTML
=====================

1 - Choose your theme method
----------------------------

Themes manage colors of SVGs on a dark or light background.

There are 2 different methods to configure themes :

- with css class (svg-theme-light or svg-theme-dark)
- with `prefers-color-scheme <https://developer.mozilla.org/fr/docs/Web/CSS/@media/prefers-color-scheme>`_


With css class
**************

::

    <link rel="stylesheet" href="https://static.snoweb.io/snowebsvg/dist/css/themes-<version>.css">

To use the latest version, replace <version> with |version|

With prefers-color-scheme
*************************

::

    <link rel="stylesheet" href="https://static.snoweb.io/snowebsvg/dist/css/themesauto-<version>.css">

To use the latest version, replace <version> with |version|


2 - Configure colors
--------------------

To define the colors of your SVGs, set your css variables as below :

::

    <style>
        :root {
            --svg-theme-light-primary: #14253A;
            --svg-theme-light-secondary: #E63946;
            --svg-theme-light-tertiary: #F7F7F7;

            --svg-theme-dark-primary: #F7F7F7;
            --svg-theme-dark-secondary: #E63946;
            --svg-theme-dark-tertiary: #112032;
        }
    </style>


The primary color is determined as the most used. Same logic for secondary and tertiary.


3 - Use animations
------------------

To use an animated SVG, you need to include the "Core" code in the `<head>` part as below :

::

    <link rel="stylesheet" href="https://static.snoweb.io/snowebsvg/dist/css/core-<version>.css">


To use the latest version, replace <version> with |version|




4 - Add SVG Content
-------------------

On your html page, add the SVG code.

SVG collections available can be found `here <https://www.snoweb-svg.com/en/>`_.

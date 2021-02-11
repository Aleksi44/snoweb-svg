.. _references_css:


CSS Helpers
===========

Trigger
-------

.svg-trigger
~~~~~~~~~~~~

Used to assign to an HTML element the hover of the child SVG animation.
For example :
::

    <a class="svg-trigger">
        <div>
            <svg>...</svg>
        </div>
    </a>

Themes
------

Colors depend on themes. For example :
::

    <svg class="svg-theme-dark">
        <path class="svg-fill-primary" d="..."></path>
        <path class="svg-fill-secondary" d="..."></path>
    </svg>


.svg-fill-primary
~~~~~~~~~~~~~~~~~

Fill primary colors with current theme.

.svg-fill-secondary
~~~~~~~~~~~~~~~~~~~

Fill secondary colors with current theme.

.svg-fill-tertiary
~~~~~~~~~~~~~~~~~~

Fill tertiary colors with current theme.

.svg-stroke-primary
~~~~~~~~~~~~~~~~~~~

Stroke primary colors with current theme.

.svg-stroke-secondary
~~~~~~~~~~~~~~~~~~~~~

Stroke secondary colors with current theme.

.svg-stroke-tertiary
~~~~~~~~~~~~~~~~~~~~

Stroke tertiary colors with current theme.


Builders
--------

.svg-builder-basic
~~~~~~~~~~~~~~~~~~

This class need to be encapsulated by ``.svg-trigger``

This class is parent of 2 children with id :

- on-start
- on-hover

This class manage opacity according to hover event.


.svg-builder-circle
~~~~~~~~~~~~~~~~~~~

This class need to be encapsulated by ``.svg-trigger``

This class need to be assign to a ``<circle>``

This class increases radius from 0 to 100 on hover event.

.. _how-to_create-svg:


Create custom SVG
=================

You need to :doc:`configure development environment <configure-dev-env>`
before doing this guide.

1 - Define the entry point
--------------------------

Each SVG depends on a collection and a group.
To define the entry point of the SVG file, you must define a path like :

``snowebsvg/collections/<collection_key>/<group_key>/<svg_key>``

For example, the rounded Finnish flag :

- collection_key : ``flag``
- group_key : ``finnish``
- svg_key : ``rounded``

The entry point of the file will therefore be :

``snowebsvg/collections/flag/finnish/rounded.html``


The command :doc:`build <../references/management-commands>` then builds automatically
depending on folders and files :

- The collection ``flag``
- The group : ``finnish``
- The svg : ``rounded``


2 - Add svg content
---------------------

In this file we could have :

::

   <svg class="svg-theme-dark">
        <path class="svg-fill-primary" d="..."></path>
        <path class="svg-fill-secondary" d="..."></path>
   </svg>


Reuse CSS, several CSS classes are available :doc:`here <../references/css>` to facilitate development.

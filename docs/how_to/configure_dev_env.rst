.. _how_to_configure_dev_env:

Configure development environment
=================================

``snowebsvg`` works with :

- `Django <https://docs.djangoproject.com/>`_
- `SASS <https://sass-lang.com/>`_

Install dependencies
--------------------

To configure your development environment, run the following :

::

    git clone git@github.com:Aleksi44/snoweb-svg.git
    pip install -r requirements.txt
    npm install


Configure Django
----------------

To configure Django, run the following :

::

    # Configure database
    python manage.py migrate

    # Import all collections
    python manage.py svg_build


Run
---

1 - Run Django server with Makefile or manually
::

    # With Makefile
    make start

    # Manually
    python manage.py runserver 0.0.0.0:4243


2 - Run Webpack server
::

    npm run start


With these commands, you have these services available :

- **SVG App** = test and view collections : ``http://localhost:8080/``


Test
----

Run Django test
::

    python manage.py test


Code style
----------

- Python : ``flake8``
- SASS : ``npm run stylelint``

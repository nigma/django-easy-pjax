Easy PJAX for Django
====================

Enhance the browsing experience of Django sites.

.. image:: https://secure.travis-ci.org/nigma/django-easy-pjax.svg?branch=master
    :target: https://secure.travis-ci.org/nigma/django-easy-pjax
    :alt: Build Status
.. image:: https://img.shields.io/pypi/v/django-easy-pjax.svg
    :target: https://pypi.python.org/pypi/django-easy-pjax/
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/dm/django-easy-pjax.svg
    :target: https://pypi.python.org/pypi/django-easy-pjax/
    :alt: Downloads
.. image:: https://img.shields.io/badge/wheel-yes-green.svg
    :target: https://pypi.python.org/pypi/django-easy-pjax/
    :alt: Wheel
.. image:: https://img.shields.io/pypi/l/django-easy-pjax.svg
    :target: https://pypi.python.org/pypi/django-easy-pjax/
    :alt: License

Developed at `en.ig.ma software shop <http://en.ig.ma>`_.

What is PJAX?
-------------

PJAX utilizes pushState and Ajax to load HTML from the server into the current
page without a full reload. It's Ajax with real permalinks, page titles,
and a working back button that fully degrades.

`Check out the demo <http://easy-pjax.herokuapp.com/>`_ that illustrates this concept
in practice and take a look at docs of `jquery-pjax`_ to get more information.

The ``django-easy-pjax`` app is a helper that makes it easy to integrate
``jquery-pjax`` with your Django 1.5+ site.

Quick Start
-----------

First include ``django-easy-pjax==1.3`` in your ``requirements.txt`` file,
add ``easy_pjax`` to your ``INSTALLED APPS`` and make sure you have
``django.template.context_processors.request`` added to template
``context_processors``.

If you are using Django 1.9+, you will also need to add the
``easy_pjax.templatetags.pjax_tags`` to template ``builtins`` in your
Django settings:

.. code-block:: python

    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [...],
            "APP_DIRS": True,
            "OPTIONS": {
                "builtins": [
                    "easy_pjax.templatetags.pjax_tags"
                ],
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.template.context_processors.static",
                    ...
                ]
            }
        }
    ]

Then simply add ``|pjax:request`` filter inside your site template ``extends`` tag::

   {% extends "theme_base.html"|pjax:request %}

The ``pjax`` filter will decide which layout template should be extended based
on HTTP headers. In the example above it will return ``theme_base.html``
for regular requests and ``pjax_base.html`` for PJAX requests.

A generic ``pjax_base.html`` template is provided by this application, but you
may need to copy it to your templates root directory and adjust it to match
your project's template blocks.

No other modification to views, code or url configuration is required,
so integration with other applications shouldn't be a problem.

The template filter also takes a comma-separated names of `base` and `pjax`
templates as the first parameter::

    {% extends "base.html,pjax_base2.html"|pjax:request %}

This is useful if you need to specify another template set.

See the ``demo.py`` file and ``tests`` directory for working examples.

Unpjax
------

``jquery-pjax`` uses cache-busting techniques and appends ``_pjax=true``
to query string params.

If for some reason you need to remove that param from query strings
you can use either the ``easy_pjax.middleware.UnpjaxMiddleware`` to remove it
from all requests before they are passed to Django views, or the ``unpjax``
filter to modify urls emitted in templates::

    <a href="{{ request.get_full_path|unpjax }}">

Documentation
-------------

The full documentation is at `django-easy-pjax.rtfd.org <http://django-easy-pjax.rtfd.org>`_.

A live demo is at `easy-pjax.herokuapp.com <https://easy-pjax.herokuapp.com/>`_.
You can run it locally after installing dependencies by running ``python demo.py``
script from the cloned repository.

Django 1.9
----------

Before Django 1.9 the ``easy-pjax`` library used the ``django.template.base.add_to_builtins``
private API to automatically register itself in the template built-ins after it was added
to the ``INSTALLED_APPS`` list.
This workaround was due to the fact that the ``{% load  %}`` tag cannot be placed before
the ``{% extends %}`` tag and the ``pjax`` template filter could not be loaded explicitly.

Starting from Django 1.9 ``easy-pjax`` does not have to rely on such workarounds because
Django now provides a clean way to add filters and tags to template
`built-ins <https://docs.djangoproject.com/es/1.9/topics/templates/#module-django.template.backends.django>`_.
This is now the recommended and the only way of installing ``easy-pjax`` template tags, also because the
`add_to_builtins API was removed <https://docs.djangoproject.com/en/1.9/releases/1.9/#django-template-base-add-to-builtins-is-removed>`_.

This is a backward incompatible change, but one that makes the integration more explicit and
following the Zen of Python.

Example of configuration settings to be used starting from Django 1.9:

.. code-block:: python

    INSTALLED_APPS = [
        "easy_pjax"
    ]
    MIDDLEWARE_CLASSES = [
        "easy_pjax.middleware.UnpjaxMiddleware"
    ]
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "builtins": [
                    "easy_pjax.templatetags.pjax_tags"
                ],
                "context_processors": [
                    "django.template.context_processors.request",
                ]
            }
        }
    ]

No changes are required for Django 1.8 or older.

License
-------

``django-easy-pjax`` is released under the BSD license.

Other Resources
---------------

- GitHub repository - https://github.com/nigma/django-easy-pjax
- PyPi Package site - http://pypi.python.org/pypi/django-easy-pjax

Please note that the `jquery-pjax`_ JavaScript library in not bundled with this
app and you still need to add proper handling to your browser-side code.

Commercial Support
------------------

This app and many other help us build better software
and focus on delivering quality projects faster.
We would love to help you with your next project so get in touch
by dropping an email at en@ig.ma.


.. _jquery-pjax: https://github.com/defunkt/jquery-pjax

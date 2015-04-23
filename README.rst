Easy PJAX for Django
====================

Enhance the browsing experience of Django sites.

.. image:: https://pypip.in/v/django-easy-pjax/badge.png
    :target: https://pypi.python.org/pypi/django-easy-pjax/
    :alt: Latest Version

.. image:: https://pypip.in/d/django-easy-pjax/badge.png
    :target: https://pypi.python.org/pypi/django-easy-pjax/
    :alt: Downloads

.. image:: https://pypip.in/license/django-easy-pjax/badge.png
    :target: https://pypi.python.org/pypi/django-easy-pjax/
    :alt: License

.. image::
    https://secure.travis-ci.org/nigma/django-easy-pjax.png?branch=master
    :alt: Build Status
    :target: https://secure.travis-ci.org/nigma/django-easy-pjax

Developed at `en.ig.ma software shop <http://en.ig.ma>`_.

What is PJAX?
-------------

PJAX utilizes pushState and Ajax to load HTML from the server into the current
page without a full reload. It's Ajax with real permalinks, page titles,
and a working back button that fully degrades.

`Check out the demo <http://easy-pjax.herokuapp.com/>`_ that illustrates this concept
in practice and take a look at docs of `jquery-pjax`_ to get more information.

The `django-easy-pjax` app is a helper that makes it trivial to integrate
`jquery-pjax` with your Django 1.5+ site.

Quick Start
-----------

Include ``django-easy-pjax`` in your requirements file, add ``easy_pjax``
to your ``INSTALLED APPS`` and make sure that you have the 
``django.core.context_processors.request`` added to ``TEMPLATE_CONTEXT_PROCESSORS``.

Then simply add ``|pjax:request`` filter inside your site template
``extends`` tag::

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

Unpjax
------

`jquery-pjax` uses cache-busting techniques and appends ``_pjax=true``
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

License
-------

`django-easy-pjax` is released under the BSD license.

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

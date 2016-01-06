#!/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script. Run:

python.exe demo.py
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os
import re

logging.basicConfig()

from django.conf import settings, global_settings
from django.conf.urls import patterns, url
from django.core.wsgi import get_wsgi_application
from django.utils.timezone import now as tznow

basename = os.path.splitext(os.path.basename(__file__))[0]


def rel(*path):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), *path)
    ).replace("\\", "/")


if not settings.configured:
    settings.configure(
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        TIMEZONE="UTC",
        DATABASES={},
        INSTALLED_APPS=[
            "django.contrib.staticfiles",
            "easy_pjax"
        ],
        MIDDLEWARE_CLASSES=[
            "easy_pjax.middleware.UnpjaxMiddleware"
        ],
        TEMPLATE_DIRS=[rel("tests", "templates", "demo")],
        TEMPLATE_CONTEXT_PROCESSORS=(
            list(global_settings.TEMPLATE_CONTEXT_PROCESSORS) +
            ["django.core.context_processors.request"]
        ),
        STATICFILES_DIRS=[rel("tests", "static")],
        STATIC_ROOT=rel("tests", "static"),
        STATICFILES_FINDERS=[
            "django.contrib.staticfiles.finders.FileSystemFinder",
            "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        ],
        STATIC_URL="/static/",
        ROOT_URLCONF=basename,
        WSGI_APPLICATION="{}.application".format(basename),
    )

from django.views.generic import TemplateView


class HelloView(TemplateView):
    template_name = "index.html"
    page_name = "Hi There!"

    def get_context_data(self, **kwargs):
        return super(HelloView, self).get_context_data(
            today=tznow(),
            page_name=self.page_name,
            **kwargs
        )

urlpatterns = patterns(
    "",
    url(r"^$", HelloView.as_view(), name="index"),
    url(r"^page-1$", HelloView.as_view(page_name="Page 1"), name="page-1"),
    url(r"^page-2$", HelloView.as_view(page_name="Page 2"), name="page-2"),
    url(r"^%s(?P<path>.*)$" % re.escape(settings.STATIC_URL.lstrip("/")),
        "django.views.static.serve", kwargs=dict(document_root=settings.STATIC_ROOT))
)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import call_command
    call_command("runserver", "8000")

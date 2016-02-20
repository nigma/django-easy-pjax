#!/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script. Run:

python.exe demo.py

Note: this demo requires Django 1.8 or higher
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

logging.basicConfig()

from django.conf import settings
from django.conf.urls import url
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
        TIMEZONE="UTC",
        DATABASES={},
        INSTALLED_APPS=[
            "django.contrib.staticfiles",
            "easy_pjax"
        ],
        MIDDLEWARE_CLASSES=[
            "easy_pjax.middleware.UnpjaxMiddleware"
        ],
        STATICFILES_DIRS=[rel("tests", "static")],
        STATIC_ROOT=rel("tests", "static-root"),
        STATICFILES_FINDERS=[
            "django.contrib.staticfiles.finders.FileSystemFinder",
            "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        ],
        STATIC_URL="/static/",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [rel("tests", "templates", "demo")],
                "APP_DIRS": True,
                "OPTIONS": {
                    "builtins": ["easy_pjax.templatetags.pjax_tags"],
                    "context_processors": [
                        "django.template.context_processors.static",
                        "django.template.context_processors.request"
                    ]
                }
            }
        ],
        ROOT_URLCONF=basename,
        WSGI_APPLICATION="{}.application".format(basename),
    )


from django.conf.urls.static import static
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

urlpatterns = [
    url(r"^$", HelloView.as_view(), name="index"),
    url(r"^page-1$", HelloView.as_view(page_name="Page 1"), name="page-1"),
    url(r"^page-2$", HelloView.as_view(page_name="Page 2"), name="page-2"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import call_command
    call_command("runserver", "8000")

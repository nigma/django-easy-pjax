#-*- coding: utf-8 -*-

"""
Register filter so it is available for use in the `extends` template tag
(The `extends` tag must come first in a template, so regular `load` is not
an option).
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from django.conf import settings

__version__ = "1.2.0"


try:
    from django.template import add_to_builtins
except ImportError:
    try:
        # import path changed in 1.8
        from django.template.base import add_to_builtins
    except ImportError:
        # No more add_to_builtins in 1.9+
        pass

if "add_to_builtins" in vars():
    add_to_builtins("easy_pjax.templatetags.pjax_tags")
else:  # Add us to builtins the django 1.9+ way
    try:
        settings.TEMPLATES[0]['OPTIONS']['builtins'].append("easy_pjax.templatetags.pjax_tags")
    except KeyError:  # No builtins defined yet
        settings.TEMPLATES[0]['OPTIONS'].update({'builtins': ["easy_pjax.templatetags.pjax_tags"]})

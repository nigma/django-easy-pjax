#-*- coding: utf-8 -*-

"""
Register filter so it is available for use in the `extends` template tag
(The `extends` tag must come first in a template, so regular `load` is not
an option).
"""

from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = "1.2.0"


try:
    from django.template import add_to_builtins
except ImportError:
    # import path changed in 1.8
    from django.template.base import add_to_builtins

add_to_builtins("easy_pjax.templatetags.pjax_tags")

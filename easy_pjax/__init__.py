#-*- coding: utf-8 -*-

"""
Register filter so it is available for use in the `extends` template tag
(The `extends` tag must come first in a template, so regular `load` is not an option).
"""

from django.template import add_to_builtins
add_to_builtins("easy_pjax.pjax_tags")

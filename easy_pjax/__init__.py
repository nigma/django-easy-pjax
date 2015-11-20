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
    for engine in settings.TEMPLATES:
        # Only modify django templates
        if engine['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
            # Create OPTIONS and OPTIONS.builtins if they are not here yet
            if 'OPTIONS' not in engine:
                engine['OPTIONS'] = {}
            if 'builtins' not in engine['OPTIONS']:
                engine['OPTIONS']['builtins'] = []
            # Do not add us if we are already in builtins
            if "easy_pjax.templatetags.pjax_tags" not in engine['OPTIONS']['builtins']:
                engine['OPTIONS']['builtins'].append("easy_pjax.templatetags.pjax_tags")

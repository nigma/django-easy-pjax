# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EasyPJAXConfig(AppConfig):
    name = 'easy_pjax'
    verbose_name = _("Easy PJAX")

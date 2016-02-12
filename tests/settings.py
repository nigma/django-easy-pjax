# -*- coding: utf-8 -*-

import django

DEBUG = False
USE_TZ = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}
INSTALLED_APPS = [
    "easy_pjax",
    "tests"
]

MIDDLEWARE_CLASSES = []
ROOT_URLCONF = "tests.urls"
SECRET_KEY = "secret"

if django.VERSION[:2] >= (1, 8):
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'builtins': ["easy_pjax.templatetags.pjax_tags"],
                'context_processors': ["django.template.context_processors.request"]
            }
        }
    ]
else:
    TEMPLATE_CONTEXT_PROCESSORS = ["django.core.context_processors.request"]

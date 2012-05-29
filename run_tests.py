#-*- coding: utf-8 -*-

import sys
from optparse import OptionParser

from django.conf import settings, global_settings

if not settings.configured:
    settings.configure(
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        INSTALLED_APPS = [
            "easy_pjax",
            "tests",
        ],
        TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS +
            ("django.core.context_processors.request",),
        ROOT_URLCONF ="tests.urls",
        DEBUG = False,
    )

from django.test.simple import DjangoTestSuiteRunner


def run_tests(*test_args, **kwargs):
    if not test_args:
        test_args = ["tests"]
    test_runner = DjangoTestSuiteRunner(
        verbosity=kwargs.get("verbosity", 1),
        interactive=kwargs.get("interactive", False),
        failfast=kwargs.get("failfast")
    )
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--failfast", action="store_true", default=False, dest="failfast")
    parser.add_option("--verbosity", action="store", default=1, type=int, dest="verbosity")
    (options, args) = parser.parse_args()
    run_tests(failfast=options.failfast, verbosity=options.verbosity, *args)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "1.2.0"

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")

setup(
    name="django-easy-pjax",
    version=version,
    description="Easy PJAX for Django.",
    license="BSD",
    author="Filip Wasilewski",
    author_email="en@ig.ma",
    url="https://github.com/nigma/django-easy-pjax",
    long_description=readme + "\n\n" + history,
    packages=[
        "easy_pjax"
    ],
    include_package_data=True,
    install_requires=[
        "django"
    ],
    zip_safe=False,
    keywords="django pjax",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    tests_require=[
        "django>=1.5",
    ],
)

#-*- coding: utf-8 -*-

from setuptools import setup

version = "1.0"

setup(
    name = "django-easy-pjax",
    version = version,
    description = "Easy PJAX for Django.",
    license = "BSD",

    author = "Filip Wasilewski",
    author_email = "en@ig.ma",

    url = "https://github.com/nigma/django-easy-pjax",
    download_url='https://github.com/nigma/django-easy-pjax/zipball/master',
    long_description = open("README.rst").read(),
    packages = ["easy_pjax"],
    include_package_data=True,
    classifiers = (
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ),
    tests_require=[
        "django>=1.4,<1.5",
    ],
    zip_safe = False
)

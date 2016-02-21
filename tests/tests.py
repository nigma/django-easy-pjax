# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf import settings
from django.test.testcases import TestCase
from django.test.client import RequestFactory, Client
from django.utils.http import urlencode


class UnpjaxMiddlewareTestCase(TestCase):

    def setUp(self):
        self.param = "1"
        self.param_encoded = urlencode({"param": self.param})

    def test_without_middleware(self):
        response = self.client.get("/unpjax/?{0}".format(self.param_encoded))
        charset = response._charset

        if charset is None:
            charset = 'UTF-8'
        content = response.content.decode(charset)
        self.assertHTMLEqual('<a href="/unpjax/?{0}">{1}</a>'.format(self.param_encoded, self.param), content)

        response = self.client.get("/unpjax/?{0}&_pjax=true".format(self.param_encoded), HTTP_X_PJAX=True)
        content = response.content.decode(charset)
        self.assertHTMLEqual('<a href="/unpjax/?{0}&_pjax=true">{1}</a>'.format(
            self.param_encoded, self.param), content)

    def test_with_middleware(self):
        MIDDLEWARE_CLASSES = list(settings.MIDDLEWARE_CLASSES) + ["easy_pjax.middleware.UnpjaxMiddleware"]

        with self.settings(MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES):
            client = Client()

            response = client.get("/unpjax/?{0}".format(self.param_encoded))
            charset = response._charset

            if charset is None:
                charset = 'UTF-8'

            content = response.content.decode(charset)
            self.assertHTMLEqual('<a href="/unpjax/?{0}">{1}</a>'.format(self.param_encoded, self.param), content)

            response = client.get("/unpjax/?{0}&_pjax=true".format(self.param_encoded), HTTP_X_PJAX=True)
            content = response.content.decode(charset)
            self.assertHTMLEqual('<a href="/unpjax/?{0}">{1}</a>'.format(self.param_encoded, self.param), content)


class UnpjaxMiddlewareNonAsciiTestCase(UnpjaxMiddlewareTestCase):

    def setUp(self):
        self.param = "xyząśżźćół"
        self.param_encoded = urlencode({"param": self.param})


class UnpjaxFilterTestCase(TestCase):

    def setUp(self):
        self.param = "1"
        self.param_encoded = urlencode({"param": self.param})

    def test_regular_request(self):
        response = self.client.get("/unpjax-filter/?{0}".format(self.param_encoded))
        charset = response._charset

        if charset is None:
            charset = 'UTF-8'

        content = response.content.decode(charset)
        self.assertHTMLEqual('<a href="/unpjax-filter/?{0}">{1}</a>'.format(self.param_encoded, self.param), content)

    def test_pjax_request(self):
        response = self.client.get("/unpjax-filter/?{0}&_pjax=true".format(self.param_encoded), HTTP_X_PJAX=True)
        charset = response._charset

        if charset is None:
            charset = 'UTF-8'

        content = response.content.decode(charset)
        self.assertHTMLEqual('<a href="/unpjax-filter/?{0}">{1}</a>'.format(self.param_encoded, self.param), content)


class UnpjaxFilterNonAsciiTestCase(UnpjaxFilterTestCase):
    def setUp(self):
        self.param = "xyząśżźćół"
        self.param_encoded = urlencode({"param": self.param})


class TemplateFilterChoiceTestCase(TestCase):
    regular_url = "/simple/?param=1"
    pjax_url = "/simple/?param=1&_pjax=true"

    def setUp(self):
        self.rf = RequestFactory()

    def build_regular_request(self):
        return self.rf.get(self.regular_url)

    def build_pjax_request(self):
        return self.rf.get(self.pjax_url, HTTP_X_PJAX=True)

    def test_template_choice_filter_with_request(self):
        from easy_pjax.templatetags.pjax_tags import pjax

        assert pjax("base.html", self.build_pjax_request()) == "pjax_base.html"
        assert pjax("base.html", self.build_regular_request()) == "base.html"

    def test_template_choice_filter_with_template_params(self):
        from easy_pjax.templatetags.pjax_tags import pjax

        assert pjax("base.html,other_pjax.html", self.build_pjax_request()) == "other_pjax.html"
        assert pjax("base.html", self.build_regular_request()) == "base.html"

    def test_template_choice_filter_with_flag(self):
        from easy_pjax.templatetags.pjax_tags import pjax

        assert pjax("base.html", True) == "pjax_base.html"
        assert pjax("base.html", False) == "base.html"


class SimpleTemplateChoiceTestCase(TestCase):
    regular_url = "/simple/?param=1"
    pjax_url = "/simple/?param=1&_pjax=true"

    def test_regular_request(self):
        resp = self.client.get(self.regular_url)
        self.assertTemplateUsed(resp, "base.html")
        self.assertTemplateNotUsed(resp, "pjax_base.html")
        self.assertContains(resp, "<div>Sample page structure</div>")
        self.assertContains(resp, "<title>Hello</title>")
        self.assertContains(resp, "<h1>Hi There!</h1>")

    def test_pjax_request(self):
        resp = self.client.get(self.pjax_url, HTTP_X_PJAX=True)
        self.assertTemplateNotUsed(resp, "base.html")
        self.assertTemplateUsed(resp, "pjax_base.html")
        self.assertNotContains(resp, "<div>Sample page structure</div>")
        self.assertContains(resp, "<title>Hello</title>")
        self.assertContains(resp, "<h1>Hi There!</h1>")


class TupleTemplateChoiceTestCase(SimpleTemplateChoiceTestCase):
    regular_url = "/tuple/?param=1"
    pjax_url = "/tuple/?param=1&_pjax=true"

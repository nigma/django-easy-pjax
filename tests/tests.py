#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.test.testcases import TestCase
from django.test.client import RequestFactory, Client


class UnpjaxMiddlewareTestCase(TestCase):
    def test_without_middleware(self):
        response = self.client.get("/unpjax/?param=1")
        content = response.content.decode(response._charset)
        self.assertHTMLEqual('<a href="/unpjax/?param=1"></a>', content)

        response = self.client.get("/unpjax/?param=1&_pjax=true", HTTP_X_PJAX=True)
        content = response.content.decode(response._charset)
        self.assertHTMLEqual('<a href="/unpjax/?param=1&_pjax=true"></a>',
                             content)

    def test_with_middleware(self):
        MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES +\
                             ("easy_pjax.middleware.UnpjaxMiddleware",)

        with self.settings(MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES):
            client = Client()

            response = client.get("/unpjax/?param=1")
            content = response.content.decode(response._charset)
            self.assertHTMLEqual('<a href="/unpjax/?param=1"></a>', content)

            response = client.get("/unpjax/?param=1&_pjax=true", HTTP_X_PJAX=True)
            content = response.content.decode(response._charset)
            self.assertHTMLEqual('<a href="/unpjax/?param=1"></a>', content)


class UnpjaxFilterTestCase(TestCase):
    def test_regular_request(self):
        response = self.client.get("/unpjax-filter/?param=1")
        content = response.content.decode(response._charset)
        self.assertHTMLEqual('<a href="/unpjax-filter/?param=1"></a>',
                             content)

    def test_pjax_request(self):
        response = self.client.get("/unpjax-filter/?param=1&_pjax=true",
            HTTP_X_PJAX=True)
        content = response.content.decode(response._charset)
        self.assertHTMLEqual('<a href="/unpjax-filter/?param=1"></a>',
                             content)


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

        assert pjax("base.html,other_pjax.html",
            self.build_pjax_request()) == "other_pjax.html"
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
        self.assertIn(b"<div>Sample page structure</div>", resp.content)
        self.assertIn(b"<title>Hello</title>", resp.content)
        self.assertIn(b"<h1>Hi There!</h1>", resp.content)

    def test_pjax_request(self):
        resp = self.client.get(self.pjax_url, HTTP_X_PJAX=True)
        self.assertTemplateNotUsed(resp, "base.html")
        self.assertTemplateUsed(resp, "pjax_base.html")
        self.assertNotIn(b"<div>Sample page structure</div>", resp.content)
        self.assertIn(b"<title>Hello</title>", resp.content)
        self.assertIn(b"<h1>Hi There!</h1>", resp.content)


class TupleTemplateChoiceTestCase(SimpleTemplateChoiceTestCase):
    regular_url = "/tuple/?param=1"
    pjax_url = "/tuple/?param=1&_pjax=true"

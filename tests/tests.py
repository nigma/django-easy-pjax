#-*- coding: utf-8 -*-

from django.conf import settings
from django.test.testcases import TestCase
from django.test.client import RequestFactory, Client


class UnpjaxMiddlewareTestCase(TestCase):
    def test_without_middleware(self):
        resp = self.client.get("/unpjax/?param=1")
        self.assertHTMLEqual('<a href="/unpjax/?param=1"></a>', resp.content)

        resp = self.client.get("/unpjax/?param=1&_pjax=true", HTTP_X_PJAX=True)
        self.assertHTMLEqual('<a href="/unpjax/?param=1&_pjax=true"></a>',
            resp.content)

    def test_with_middleware(self):
        MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES +\
                             ("easy_pjax.middleware.UnpjaxMiddleware",)

        with self.settings(MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES):
            client = Client()

            resp = client.get("/unpjax/?param=1")
            self.assertHTMLEqual('<a href="/unpjax/?param=1"></a>',
                resp.content)

            resp = client.get("/unpjax/?param=1&_pjax=true", HTTP_X_PJAX=True)
            self.assertHTMLEqual('<a href="/unpjax/?param=1"></a>',
                resp.content)

            # _pjax_ is not _pjax, should stay
            resp = self.client.get("/unpjax/?param=1&_pjax_=true",
                HTTP_X_PJAX=True)
            self.assertHTMLEqual('<a href="/unpjax/?param=1&_pjax_=true"></a>',
                resp.content)


class UnpjaxFilterTestCase(TestCase):
    def test_regular_request(self):
        resp = self.client.get("/unpjax-filter/?param=1")
        self.assertHTMLEqual('<a href="/unpjax-filter/?param=1"></a>',
            resp.content)

    def test_pjax_request(self):
        resp = self.client.get("/unpjax-filter/?param=1&_pjax=true",
            HTTP_X_PJAX=True)
        self.assertHTMLEqual('<a href="/unpjax-filter/?param=1"></a>',
            resp.content)

        # _pjax_ is not _pjax, should stay
        resp = self.client.get("/unpjax-filter/?param=1&_pjax_=true",
            HTTP_X_PJAX=True)
        self.assertHTMLEqual(
            '<a href="/unpjax-filter/?param=1&_pjax_=true"></a>', resp.content)


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
        from easy_pjax.pjax_tags import pjax

        assert pjax("base.html", self.build_pjax_request()) == "pjax_base.html"
        assert pjax("base.html", self.build_regular_request()) == "base.html"

    def test_template_choice_filter_with_template_params(self):
        from easy_pjax.pjax_tags import pjax

        assert pjax("base.html,other_pjax.html",
            self.build_pjax_request()) == "other_pjax.html"
        assert pjax("base.html", self.build_regular_request()) == "base.html"

    def test_template_choice_filter_with_flag(self):
        from easy_pjax.pjax_tags import pjax

        assert pjax("base.html", True) == "pjax_base.html"
        assert pjax("base.html", False) == "base.html"


class SimpleTemplateChoiceTestCase(TestCase):
    regular_url = "/simple/?param=1"
    pjax_url = "/simple/?param=1&_pjax=true"

    def test_regular_request(self):
        resp = self.client.get(self.regular_url)
        self.assertTemplateUsed(resp, "base.html")
        self.assertTemplateNotUsed(resp, "pjax_base.html")
        self.assertIn("<div>Sample page structure</div>", resp.content)
        self.assertIn("<title>Hello</title>", resp.content)
        self.assertIn("<h1>Hi There!</h1>", resp.content)

    def test_pjax_request(self):
        resp = self.client.get(self.pjax_url, HTTP_X_PJAX=True)
        self.assertTemplateNotUsed(resp, "base.html")
        self.assertTemplateUsed(resp, "pjax_base.html")
        self.assertNotIn("<div>Sample page structure</div>", resp.content)
        self.assertIn("<title>Hello</title>", resp.content)
        self.assertIn("<h1>Hi There!</h1>", resp.content)


class TupleTemplateChoiceTestCase(SimpleTemplateChoiceTestCase):
    regular_url = "/tuple/?param=1"
    pjax_url = "/tuple/?param=1&_pjax=true"

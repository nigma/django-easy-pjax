#-*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns("",
    url(r"^simple/", TemplateView.as_view(template_name="site_base.html")),
    url(r"^tuple/$", TemplateView.as_view(template_name="site_base2.html")),
    url(r"^unpjax/", TemplateView.as_view(template_name="unpjax_middleware.html")),
    url(r"^unpjax-filter/", TemplateView.as_view(template_name="unpjax_filter.html")),
)

#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.http import QueryDict


class UnpjaxMiddleware(object):
    """
    Removes the `_pjax` parameter from query string
    """

    def process_request(self, request):
        if "_pjax" in request.META.get("QUERY_STRING", ""):
            qs = QueryDict(request.META.get("QUERY_STRING", ""),
                           encoding=request.encoding, mutable=True)
            qs.pop("_pjax", None)
            request.META["QUERY_STRING"] = qs.urlencode()

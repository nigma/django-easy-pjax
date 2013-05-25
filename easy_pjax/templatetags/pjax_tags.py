#-*- coding: utf-8 -*-

from django import template
from django.http import QueryDict

# Note: this file is automatically added to Django template builtins
# by the easy_pjax.__init__ module.

register = template.Library()


@register.filter_function
def pjax(template_names, request, default="pjax_base.html"):
    """
    Returns template name for request.

    :param request: Django request or boolean value
    :param template_names: Base theme name or comma-separated names of base and
      pjax templates.

    Examples::

        {% extends "base.html"|pjax:request %}
        {% extends "base.html,pjax_base.html"|pjax:request %}

        context = {"is_pjax": True}
        {% extends "base.html"|pjax:is_pjax %}
    """
    if isinstance(request, (bool, int)):
        is_pjax = request
    else:
        is_pjax = request.META.get("HTTP_X_PJAX", False)
    
    template_name, pjax_template_name = template_names.split(',', 1)

    if is_pjax:
        return pjax_template_name.strip() or default
    return template_name.strip()


@register.filter_function
def unpjax(url):
    """
    Removes `_pjax` param from query string of a given url::

        <a href="{{ request.get_full_path|unpjax }}"></a>
    """
    if "?" in url:
        base, qs = url.split("?", 1)
        if "_pjax" in qs:
            qs = QueryDict(qs, mutable=True)
            qs.pop("_pjax", None)
            qs = qs.urlencode()
            if qs:
                return base + "?" + qs
            return base
    return url

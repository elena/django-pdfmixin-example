# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from django.views.generic.base import TemplateResponseMixin

from pages.models import Page
from pages.pdfs import render_to_pdf


class PDFResponseMixin(TemplateResponseMixin):
    """
    Mixin for Django class based views.
    Switch normal and pdf template based on request.

    The switch is made when the request has a particular querydict, per
    class attributes, `pdf_querydict_keys` and `pdf_querydict_value`
    example:

        http://www.example.com?[pdf_querydict_key]=[pdf_querydict_value]

    Example with values::

        http://www.example.com?format=pdf

    Simplified version of snippet here:
    http://djangosnippets.org/snippets/2540/
    """
    pdf_querydict_key = 'format'
    pdf_querydict_value = 'pdf'

    def is_pdf(self):
        value = self.request.REQUEST.get(self.pdf_querydict_key, '')
        return value.lower() == self.pdf_querydict_value.lower()

    def get_pdf_response(self, context, **response_kwargs):
        model_object = context[self.context_object_name]
        return render_to_pdf(model_object)

    def render_to_response(self, context, **response_kwargs):
        if self.is_pdf():
            from django.conf import settings
            context['STATIC_ROOT'] = settings.STATIC_ROOT
            return self.get_pdf_response(context, **response_kwargs)
        #context[self.pdf_url_varname] = self.get_pdf_url()
        return super(PDFResponseMixin, self).render_to_response(
            context, **response_kwargs)


class DetailView(PDFResponseMixin, DetailView):

    model = Page
    slug_field = 'slug'


django-pdfmixin-example
=======================

Django CBV simple PDF mixin example project.

""" This is based on the case scenario where you have a model which has a
`DetailView`, but a "bespoke" PDF for the same model is also created that is
not dependent on the `DetailView` (except to provide the query object).

The PDF needs to be returned as a `HTTPResponse` object. The model object is
provided.

Working project example: https://github.com/elena/django-pdfmixin-example

Credit: For the case scenario to convert HTML pages to PDFs see this snippet
(from which this snippet largely drew upon):
http://djangosnippets.org/snippets/2540/
"""

## Model

    from django.db import models

    class Page(models.Model):
        title = models.CharField(max_length=30)
        slug = models.SlugField()
        # ...


## PDF

    # -*- coding: utf-8 -*-
    from django.http import HttpResponse
    from reportlab.pdfgen import canvas

    def render_to_pdf(my_page):
        """ https://docs.djangoproject.com/en/dev/howto/outputting-pdf/ """

        response = HttpResponse(content_type='application/pdf')
        # uncomment to toggle: downloading | display (moz browser)
        # response['Content-Disposition'] = 'attachment; filename="myfilename.pdf"'

        c = canvas.Canvas(response)
        c.drawString(100, 600, my_page.title)
        c.showPage
        c.save()
        return response


## URL

    # -*- coding: utf-8 -*-
    from django.conf.urls import url, patterns
    from .views import DetailView

    urlpatterns = patterns('',
        url(r'^page/(?P<slug>[\w/-]+)$', DetailView.as_view(),
            name='page_detail'),
    )


## View

    # -*- coding: utf-8 -*-
    from django.views.generic import DetailView
    from django.views.generic.base import TemplateResponseMixin

    from .models import Page
    from .pdfs import render_to_pdf


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
            return render_to_pdf(self.get_object())

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


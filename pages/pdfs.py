# -*- coding: utf-8 -*-
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def render_to_pdf(my_page):
    """ https://docs.djangoproject.com/en/dev/howto/outputting-pdf/ """
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    c = canvas.Canvas(response)
    c.drawString(100, 600, my_page.title)
    c.showPage
    c.save()
    return response

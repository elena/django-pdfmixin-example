# -*- coding: utf-8 -*-
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def hello(c, my_page):
    """ http://www.reportlab.com/docs/reportlab-userguide.pdf
    Example from page 11.
    """
    from reportlab.lib.units import inch
    c.translate(inch,inch)
    c.setFont("Helvetica", 14)
    c.setStrokeColorRGB(0.2,0.5,0.3)
    c.setFillColorRGB(1,0,1)
    c.line(0,0,0,1.7*inch)
    c.line(0,0,1*inch,0)
    c.rect(0.2*inch,0.2*inch,1*inch,1.5*inch, fill=1)
    c.rotate(90)
    c.setFillColorRGB(0,0,0.77)
    c.drawString(0.3*inch, -inch, "Hello World")

    c.drawString(inch, 2*inch, my_page.title)


def render_pdf(my_page):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    c = canvas.Canvas(response)
    hello(c, my_page)
    c.showPage
    c.save()
    return response

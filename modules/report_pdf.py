#!/usr/bin/env python
# -*- coding: utf8 -*-

from fpdf import FPDF


class Report(FPDF):

    def __init__(self, head_title):
        super(Report, self).__init__()
        self.head_title = head_title

    def header(self):
        # Logo
        #self.image('logo_pb.png',10,8,33)
        # Arial bold 15
        #self.add_font('DejaVu','','DejaVuSansCondensed.ttf',uni=True)
        #self.set_font('DejaVu','',14)
        self.set_font('Arial', 'B', 14)
        #print self.title.encode('utf-8')
        # Move to the right
        #self.cell(80)
        # Title
        title = u''
        if self.head_title == 1:
            title = u'Formato de Proyecto'
        elif self.head_title == 2:
            title = u'Resultado de Proyecto'
        #self.cell(0,10,u'Informe Oftalmológico',0,0,'C')
        self.cell(0, 10, title, 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        self.set_y(-20)
        #Arial 12
        #self.set_font('Arial', '', 8)
        #Background color
        self.set_fill_color(0, 200, 0)
        self.set_line_width(0.1)
        #Title
        self.cell(0, 1, '', 0, 1, 'L', 1)
        #Line break
        self.ln(1)
        # Position at 1.5 cm from bottom
        #self.set_line_width(0.2)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 4, u'Página %s/{nb}' % self.page_no(), 0, 1, 'C')
        self.cell(0, 4, u'CIMA ONG', 0, 1)
        self.cell(0, 4, u'Tarapoto', 0, 1)
        self.cell(0, 4, u'Telefono:', 0, 1)


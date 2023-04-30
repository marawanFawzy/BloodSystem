from flask import *
import os
from database import get_db
import lib
import pdfkit


def post():
    try:
        body = request.form['body']
        lab_code = request.form['lab_code']
        config = pdfkit.configuration(
            wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        _html = '<html><body><h1>Hello ' + lab_code+'</h1></body></html>'  # design
        data = {}
        body = body.split(',')
        i = 0
        for el in body:
            el = el.split(':')

            if i == 0:
                data[el[0][2:-1]] = el[1][1:-1]
            elif i == len(body)-1:
                data[el[0][1:-1]] = el[1][1:-2]
            else:
                data[el[0][1:-1]] = el[1][1:-1]
            print(data)
            i = i+1

        pdfkit.from_string(_html, 'reports/'+str(lab_code) +
                           '_report.pdf', configuration=config)

        os.startfile(os.path.join('reports',
                                  str(lab_code) + '_report.pdf'), "print")
        r = '<span class="success">Done.</span>'
        return r
    except Exception as error:
        print(error)
        return '<span class="error">Server Error: %s</span>' % error

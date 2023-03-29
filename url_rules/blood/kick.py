from flask import *

from database import get_db


def post():
    try:
        db = get_db('database')
        sheet_code = request.form['sheet_code'].strip().lower()
        lab_code = request.form['lab_code'].strip().lower()
        if not (sheet_code and lab_code):
            return '<span class="error">ERROR: Use two codes to kick</span>'
        if sheet_code and lab_code:
            test = db.execute(
                'SELECT * FROM patient_in WHERE Sheet_Code=? and Lab_Code=?', (sheet_code, lab_code)).fetchall()
            if not test:
                return '<span class="error">ERROR: Sheet code not in blood lab</span>'
            db.execute('DELETE FROM patient_out WHERE Lab_Code=?', (lab_code,))
            db.execute('DELETE FROM patient_in WHERE sheet_code=?',
                       (sheet_code,))
            return '<span class="success">Done.</span>'
    except Exception as error:
        return '<span class="error">Server Error: %s</span>' % error

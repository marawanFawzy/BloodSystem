from flask import *

from database import get_db


def post():
    try:
        tubes = request.form['tubes'].strip().lower()
        lab_code = request.form['lab_code'].strip().lower()
        db = get_db('database')
        db.execute('UPDATE patient_in SET Tubes =? WHERE Lab_Code =? ', (
            tubes,
            lab_code
        ))
        # db.execute('UPDATE patients SET stage=2 WHERE code=?', (sheet_code,))
        r = '<span class="success">Done.</span>'
        return r
    except Exception as error:
        return '<span class="error">Server Error: %s</span>' % error

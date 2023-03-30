from flask import *
import os
from database import get_db


def post():
    try:
        db = get_db('database')
        if request.url_root.__contains__(request.access_route[0]) or True:
            print("admin")
            sheet_code = request.form['sheet_code'].strip().lower()
            lab_code = request.form['lab_code'].strip().lower()
            if not (sheet_code and lab_code):
                return '<span class="error">ERROR: Use two codes to kick</span>'
            if sheet_code and lab_code:
                test = db.execute(
                    'SELECT * FROM patient_in WHERE Sheet_Code=? and Lab_Code=?', (sheet_code, lab_code)).fetchall()
                if not test:
                    return '<span class="error">ERROR: Sheet code not in blood lab</span>'
                file = os.path.join(os.path.join(
                    app.config['UPLOAD_FOLDER'], lab_code+".png"))
                if os.path.isfile(file):
                    os.remove(file)
                db.execute(
                    'DELETE FROM patient_out WHERE Lab_Code=?', (lab_code,))
                db.execute('DELETE FROM patient_in WHERE sheet_code=?',
                           (sheet_code,))
                return '<span class="success">Done.</span>'
        else:
            return '<span class="error">only admin can do this</span>'
    except Exception as error:
        return '<span class="error">Server Error: %s</span>' % error

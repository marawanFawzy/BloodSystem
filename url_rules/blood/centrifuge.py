from flask import *

from database import get_db
import lib


def get():
    try:
        lab_code = request.args.get('lab_code')
        value = request.args.get('value')
        db = get_db('database')
        db.execute('UPDATE patient_in SET Tubes =?, Centrifuged =1 , Date_Centrifuged =? WHERE Lab_Code =? ', (
            value,
            lib.time(),
            lab_code
        ))
        # db.execute('UPDATE patients SET stage=2 WHERE code=?', (sheet_code,))
        r = '<span class="success">Done.</span>'
        return r
    except Exception as error:
        return '<span class="error">Server Error: %s</span>' % error

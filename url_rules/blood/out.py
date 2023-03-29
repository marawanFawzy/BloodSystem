from flask import *

from database import get_db
import lib


def get():
    try:
        db = get_db('database')
        lab_code = request.args.get('lab_code')
        filter = request.args.get('filter')
        value = request.args.get('value')
        db.execute('UPDATE patient_out SET '+filter+'=? , Timestamp = ?, Date = ?  WHERE Lab_Code=?',
                   (value, lib.time(), lib.date(), lab_code,))
        return '<span class="success">Done.</span>'
    except Exception as error:
        return '<span class="error">Server Error: %s</span>' % error

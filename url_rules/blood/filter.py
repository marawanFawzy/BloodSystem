from flask import *

import json

from database import get_db


def get():
    filter = request.args.get('filter')
    db = get_db('database')
    row = db.execute('SELECT o.Lab_Code FROM patient_out o JOIN patient_in i ON o.Lab_Code = i.Lab_Code WHERE o.'
                     + filter+'="-1" ORDER BY i.timestamp').fetchall()
    return json.dumps(row)

from flask import *

import json

from database import get_db
import lib


def get():
    data = []
    db = get_db('database')
    for row in db.execute(
        'SELECT * FROM patient_in i JOIN patient_out o ON i.Lab_Code = o.Lab_Code ORDER BY i.timestamp'
    ).fetchall():
        row = list(row)
        row[2] = lib.str_time(row[2])
        row[9] = lib.str_time(row[9])
        data.append(row)
    return json.dumps(data)

from flask import *

import json

from database import get_db
import lib


def get():
    data = []
    db = get_db('database')
    for row in db.execute(
        'SELECT * FROM patient_in i JOIN patient_out o ON i.Lab_Code = o.Lab_Code ORDER BY Date_Centrifuged , i.Timestamp'
    ).fetchall():
        row = list(row)
        row[2] = lib.str_time(row[2])
        # row 1 is sheet coe but it is not used so it holds the timestamp of Date_Centrifuged to chek on it 
        row[1] = row[7]
        row[7] = lib.str_time(row[7])
        row[9] = lib.str_time(row[9])
        data.append(row)
    return json.dumps(data)

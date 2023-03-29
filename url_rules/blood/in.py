from flask import *
from database import get_db

import lib


def post():
    Hepatitis = -10
    CBC = -10
    Albumin = -10
    GPT = -10
    PT = -10
    Bilirubin_direct = -10
    Bilirubin_total = -10
    Creatinine = -10
    Urea = -10
    Uric = -10
    Glucose = -10
    HBA1C = -10
    ESR = -10
    TAG = -10
    Total_cholesterol = -10
    Hpp = -10
    ASOT = -10
    CRP = -10
    LDL = -10
    HDL = -10
    flags = ""
    try:
        sheet_code = request.form['sheet_code'].strip().lower()
        lab_code = request.form['lab_code'].strip().lower()
        if 'Hepatitis' in request.form:
            flags += 'Hepatitis - '
            Hepatitis = -1
        if 'CBC' in request.form:
            flags += 'CBC - '
            CBC = -1
        if 'Albumin' in request.form:
            flags += 'Albumin - '
            Albumin = -1
        if 'GPT' in request.form:
            flags += 'GPT - '
            GPT = -1
        if 'PT' in request.form:
            flags += 'PT - '
            PT = -1
        if 'Bilirubin_direct' in request.form:
            flags += 'Bilirubin_direct - '
            Bilirubin_direct = -1
        if 'Bilirubin_total' in request.form:
            flags += 'Bilirubin_total - '
            Bilirubin_total = -1
        if 'Creatinine' in request.form:
            flags += 'Creatinine - '
            Creatinine = -1
        if 'Urea' in request.form:
            flags += 'Urea - '
            Urea = -1
        if 'Uric' in request.form:
            flags += 'Uric - '
            Uric = -1
        if 'Glucose' in request.form:
            flags += 'Glucose - '
            Glucose = -1
        if 'ESR' in request.form:
            flags += 'ESR - '
            ESR = -1
        if 'TAG' in request.form:
            flags += 'TAG - '
            TAG = -1
        if 'HBA1C' in request.form:
            flags += 'HBA1C - '
            HBA1C = -1
        if 'Total_cholesterol' in request.form:
            flags += 'Total_cholesterol - '
            Total_cholesterol = -1
        if 'Hpp' in request.form:
            flags += '2Hpp - '
            Hpp = -1
        if 'ASOT' in request.form:
            flags += 'ASOT - '
            ASOT = -1
        if 'CRP' in request.form:
            flags += 'CRP - '
            CRP = -1
        if 'LDL' in request.form:
            flags += 'LDL - '
            LDL = -1
        if 'HDL' in request.form:
            flags += 'HDL - '
            HDL = -1

        db = get_db('database')
        db.execute('INSERT INTO patient_in (Lab_Code, Sheet_Code, Date, Timestamp, Required_Analysis) VALUES (?, ?, ?, ?, ?)', (
            lab_code,
            sheet_code,
            lib.date(),
            lib.time(),
            flags
        ))
        db.execute(
            'INSERT INTO patient_out (Lab_Code,Timestamp,Date,Hepatitis,CBC,Albumin,GPT,PT,Bilirubin_direct,Bilirubin_total,Creatinine,Urea,Uric,Glucose,ESR,TAG,HBA1C,Total_Cholesterol,Hpp,ASOT,CRP,LDL,HDL) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (
                lab_code, lib.time(), lib.date(),
                Hepatitis, CBC, Albumin, GPT, PT, Bilirubin_direct,
                Bilirubin_total, Creatinine, Urea, Uric,
                Glucose, ESR, TAG, HBA1C, Total_cholesterol,
                Hpp, ASOT, CRP, LDL, HDL
            ))
        # db.execute('UPDATE patients SET stage=2 WHERE code=?', (sheet_code,))
        r = '<span class="success">Done.</span>'
        return r
    except Exception as error:
        return '<span class="error">Server Error: %s</span>' % error

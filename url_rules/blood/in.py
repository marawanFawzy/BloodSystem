from flask import *
from database import get_db

import lib


def post():
    if request.url_root.__contains__(request.access_route[0]) or True:
        db = get_db('database')
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
        update = False
        try:
            sheet_code = request.form['sheet_code'].strip().lower()
            lab_code = request.form['lab_code'].strip().lower()
            if 'old' in request.form:
                update = True
                x = db.execute(
                    'SELECT * FROM patient_in i JOIN patient_out o ON i.Lab_Code = o.Lab_Code WHERE i.Sheet_Code=? and i.Lab_Code=? ORDER BY i.timestamp', (
                        sheet_code, lab_code)
                ).fetchall()
                x = list(x[0])
                flags = x[4]
                Hepatitis = x[11]
                CBC = x[12]
                Albumin = x[13]
                GPT = x[14]
                PT = x[15]
                Bilirubin_direct = x[16]
                Bilirubin_total = x[17]
                Creatinine = x[18]
                Urea = x[19]
                Uric = x[20]
                Glucose = x[21]
                ESR = x[22]
                TAG = x[23]
                HBA1C = x[24]
                Total_cholesterol = x[25]
                Hpp = x[26]
                ASOT = x[27]
                CRP = x[28]
                LDL = x[29]
                HDL = x[30]
            else:
                flags = ""
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
            if update:
                print("add to database")
                db.execute(
                    'UPDATE patient_in SET Required_Analysis = ? , Centrifuged= 0 , Date_Centrifuged=0 WHERE Lab_Code=?' , (flags,lab_code,))
                db.execute('UPDATE patient_out SET Hepatitis=?,CBC=?,Albumin=?,GPT=?,PT=?,Bilirubin_direct=?,Bilirubin_total=?,Creatinine=?,Urea=?,Uric=?,Glucose=?,ESR=?,TAG=?,HBA1C=?,Total_Cholesterol=?,Hpp=?,ASOT=?,CRP=?,LDL=?,HDL=? WHERE Lab_Code=?', (
                    Hepatitis, CBC, Albumin, GPT, PT, Bilirubin_direct,
                    Bilirubin_total, Creatinine, Urea, Uric,
                    Glucose, ESR, TAG, HBA1C, Total_cholesterol,
                    Hpp, ASOT, CRP, LDL, HDL, lab_code
                ))
                r = '<span class="success">tests added to patient.</span>'
            else:
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
    else:
        return '<span class="error">only admin can do this</span>'

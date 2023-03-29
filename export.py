import xlsxwriter
import json
import sqlite3
db = sqlite3.connect('database.sqlitedb')

index = {}
data = []

blood_mia = []
urine_mia = []
stool_mia = []
pharm_mia = []


for code, name, age, gender, flags in db.execute(
        'SELECT code, name, age, gender, flags FROM patients').fetchall():

    entry = dict(
        code='',
        name='',
        age='',
        gender='',
        flags='',
        blood_lab_code='',
        blood_has_left='',
        blood_urea='',
        blood_creatinine='',
        blood_uric='',
        blood_albumin='',
        blood_bilirubin_direct='',
        blood_bilirubin_total='',
        blood_glucose='',
        blood_pt='',
        blood_asot='',
        blood_cbc='',
        blood_gpt='',
        blood_crp='',
        blood_hepatitis='',
        blood_esr='',
        urine_has_left='',
        urine_rbc='',
        urine_pus='',
        urine_epith='',
        urine_cast='',
        urine_ca_ox='',
        urine_phosph='',
        urine_uric='',
        urine_amorph='',
        urine_other='',
        stool_lab_code='',
        stool_has_left='',
        stool_ehistolytica='',
        stool_ecoli='',
        stool_glamblia='',
        stool_enterobius='',
        stool_hnana='',
        stool_taenia='',
        stool_ancylostoma='',
        stool_fasciola='',
        stool_ascaris='',
        stool_schmansoni='',
        stool_other='',
        pharm_diagnosis='',
        pharm_drugs=''
    )
    index[code] = entry
    data.append(entry)

    entry['code'] = code
    entry['name'] = name
    entry['age'] = age
    entry['gender'] = gender
    entry['flags'] = flags


for sheet_code, lab_code, hasleft in db.execute(
        'SELECT sheet_code, lab_code, hasleft FROM blood_in').fetchall():

    if not sheet_code in index:
        blood_mia.append(sheet_code)
        continue

    entry = index[sheet_code]
    entry['blood_lab_code'] = lab_code
    entry['blood_has_left'] = hasleft

    if hasleft:
        for urea, creatinine, uric, albumin, bilirubin_direct, bilirubin_total,\
            glucose, pt, asot, cbc, gpt, crp, hepatitis, esr in db.execute(
                'SELECT urea, creatinine, uric, albumin, bilirubin_direct,' +
                ' bilirubin_total, glucose, pt, asot, cbc, gpt, crp,' +
                ' hepatitis, esr FROM blood_out WHERE code=?',
                (sheet_code,)).fetchall():
            entry['blood_urea'] = urea
            entry['blood_creatinine'] = creatinine
            entry['blood_uric'] = uric
            entry['blood_albumin'] = albumin
            entry['blood_bilirubin_direct'] = bilirubin_direct
            entry['blood_bilirubin_total'] = bilirubin_total
            entry['blood_glucose'] = glucose
            entry['blood_pt'] = pt
            entry['blood_asot'] = asot
            entry['blood_cbc'] = cbc
            entry['blood_gpt'] = gpt
            entry['blood_crp'] = crp
            entry['blood_hepatitis'] = hepatitis
            entry['blood_esr'] = esr


for sheet_code, lab_code, hasleft in db.execute(
        'SELECT sheet_code, lab_code, hasleft FROM urine_in').fetchall():

    if not sheet_code in index:
        urine_mia.append(sheet_code)
        continue

    entry = index[sheet_code]
    entry['urine_lab_code'] = lab_code
    entry['urine_has_left'] = hasleft

    if hasleft:
        for rbc, pus, epith, cast, ca_ox, phosph, uric, amorph, other in \
            db.execute(
                'SELECT rbc, pus, epith, `cast`, ca_ox, phosph, uric,' +
                ' amorph, other FROM urine_out WHERE code=?',
                (sheet_code,)).fetchall():
            entry['urine_rbc'] = rbc
            entry['urine_pus'] = pus
            entry['urine_epith'] = epith
            entry['urine_cast'] = cast
            entry['urine_ca_ox'] = ca_ox
            entry['urine_phosph'] = phosph
            entry['urine_uric'] = uric
            entry['urine_amorph'] = amorph
            entry['urine_other'] = other


for sheet_code, lab_code, hasleft in db.execute(
        'SELECT sheet_code, lab_code, hasleft FROM stool_in').fetchall():

    if not sheet_code in index:
        stool_mia.append(sheet_code)
        continue

    entry = index[sheet_code]
    entry['stool_lab_code'] = lab_code
    entry['stool_has_left'] = hasleft

    if hasleft:
        for ehistolytica, ecoli, glamblia, enterobius, hnana, taenia, \
            ancylostoma, fasciola, ascaris, schmansoni, other in \
            db.execute(
                'SELECT ehistolytica, ecoli, glamblia, enterobius, hnana, ' +
                'taenia, ancylostoma, fasciola, ascaris, schmansoni, other' +
                ' FROM stool_out WHERE code=?',
                (sheet_code,)).fetchall():
            entry['stool_ehistolytica'] = ehistolytica
            entry['stool_ecoli'] = ecoli
            entry['stool_glamblia'] = glamblia
            entry['stool_enterobius'] = enterobius
            entry['stool_hnana'] = hnana
            entry['stool_taenia'] = taenia
            entry['stool_ancylostoma'] = ancylostoma
            entry['stool_fasciola'] = fasciola
            entry['stool_ascaris'] = ascaris
            entry['stool_schmansoni'] = schmansoni
            entry['stool_other'] = other


def parse_drugs(drugs):
    result = ''
    drugs = json.loads(drugs)
    for d in drugs:
        result += '%s x%d, ' % (d, drugs[d])
    return result[:-2]


for code, diagnosis, drugs in db.execute(
        'SELECT code, diagnosis, drugs FROM pharmacy_out').fetchall():

    if not code in index:
        pharm_mia.append(code)
        continue

    entry = index[code]
    entry['pharm_diagnosis'] = diagnosis
    entry['pharm_drugs'] = parse_drugs(drugs)


book = xlsxwriter.Workbook('data_export.xlsx')
sheet = book.add_worksheet('data')
head = ('code', 'name', 'age', 'gender', 'flags', 'blood_lab_code',
        'blood_has_left', 'blood_urea', 'blood_creatinine', 'blood_uric',
        'blood_albumin', 'blood_bilirubin_direct', 'blood_bilirubin_total',
        'blood_glucose', 'blood_pt', 'blood_asot', 'blood_cbc', 'blood_gpt',
        'blood_crp', 'blood_hepatitis', 'blood_esr', 'urine_lab_code',
        'urine_has_left', 'urine_rbc', 'urine_pus', 'urine_epith',
        'urine_cast', 'urine_ca_ox', 'urine_phosph', 'urine_uric',
        'urine_amorph', 'urine_other', 'stool_lab_code', 'stool_has_left',
        'stool_ehistolytica', 'stool_ecoli', 'stool_glamblia',
        'stool_enterobius', 'stool_hnana', 'stool_taenia', 'stool_ancylostoma',
        'stool_fasciola', 'stool_ascaris', 'stool_schmansoni', 'stool_other',
        'pharm_diagnosis', 'pharm_drugs')

for i in range(len(head)):
    sheet.write(0, i, head[i])

for d in range(len(data)):
    for i in range(len(head)):
        sheet.write(d+1, i, data[d][head[i]])

book.close()


with open('mia_report.txt', 'w', encoding='utf-8') as file:
    file.write('Blood lab MIA count: %d\n' % len(blood_mia))
    file.write('Urine lab MIA count: %d\n' % len(urine_mia))
    file.write('Stool lab MIA count: %d\n' % len(stool_mia))
    file.write('Pharmacy  MIA count: %d\n' % len(pharm_mia))
    file.write('\n\n')
    file.write('Blood lab MIA Codes:\n')
    for code in blood_mia:
        file.write(code + '\n')
    file.write('\n\n')
    file.write('Urine lab MIA Codes:\n')
    for code in urine_mia:
        file.write(code + '\n')
    file.write('\n\n')
    file.write('Stool lab MIA Codes:\n')
    for code in stool_mia:
        file.write(code + '\n')
    file.write('\n\n')
    file.write('Pharmacy MIA Codes:\n')
    for code in pharm_mia:
        file.write(code + '\n')


print('EXPORT COMPLETE!')

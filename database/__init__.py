import os
import sqlite3

from flask import g


def get_db(db_name):
    if not getattr(g, 'db_' + db_name, False):
        uri = os.path.join('database.sqlitedb')
        # db  = sqlite3.connect('%s?mode=%s' %(uri, mode), uri=True)
        db = sqlite3.connect(uri)
        setattr(g, 'db_' + db_name, db)
    return db


def close_all_db():
    for db_name in filter(lambda x: x.startswith('db_'), dir(g)):
        db = getattr(g, db_name)
        db.commit()
        db.close()
    return

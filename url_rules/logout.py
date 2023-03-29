from flask import *


def get():
    session.pop('username', None)
    session.pop('loggedin', None)
    return render_template('app.html')

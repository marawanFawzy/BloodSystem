from flask import *

requires = 'login'


def get():
    return render_template('app.html')

from flask import session, flash, redirect, url_for, render_template

powers = {
}

# entry


def require_auth(auth, function):
    def f(*args, **kwargs):
        if 'login' in auth:
            return render_template('app.html')

        return function(*args, **kwargs)

    return f

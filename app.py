# Disable imported-modules compilation
import logs
import database
import lib
import core
import flask
import sys

sys.dont_write_bytecode = True

# Create Flask application

app = flask.Flask(__name__)
app.config.from_object('core.config')

# Import stuff

# Load url-rules
special_refs = dict(
    app=app,
    lib=lib,
    get_db=database.get_db,
    log=logs.log
)

core.url_loader.load_from(app.config['DIR_URL_RULES'], app, **special_refs)

# Export stuff to Jinja2
app.jinja_env.globals.update(
)


# Request handlers
@app.teardown_request
def teardown_request(exception):
    database.close_all_db()
    return


# Start WebApp
if __name__ == '__main__':
    app.run(**core.config.SERVING_OPTIONS)

DEBUG = True
SECRET_KEY = 'HayahSoft'
DIR_URL_RULES = 'url_rules'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///database/database.db'

if DEBUG:
    SERVING_OPTIONS = dict(
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
else:
    SERVING_OPTIONS = dict(
        host='0.0.0.0',
        port=5000,
        threaded=True
    )

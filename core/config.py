DEBUG = False
SECRET_KEY = 'HayahSoft'
DIR_URL_RULES = 'url_rules'
STATIC_FOLDER = 'C:\\Users\\maraw\\Desktop\\7yah\\BloodSystem\\Hayah 51 Software\\static'
UPLOAD_FOLDER = 'C:\\Users\\maraw\\Desktop\\7yah\\BloodSystem\\Hayah 51 Software\\static\\uploads'

# SQLALCHEMY_DATABASE_URI = 'sqlite:///database/database.db'

if DEBUG:
    SERVING_OPTIONS = dict(
        host='0.0.0.0',
        port=3200,
        threaded=True
    )
else:
    SERVING_OPTIONS = dict(
        host='0.0.0.0',
        port=3200,
        threaded=True
    )

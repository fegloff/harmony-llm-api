from flask import Flask
from flask_session import Session
from flask_cors import CORS
from apis import api
from models import db
import config as app_config
from res import PdfFileInvalidFormat
import os

app = Flask(__name__)

app.app_context().push()

app.config['SECRET_KEY']=app_config.config.SECRET_KEY
app.config['SESSION_PERMANENT'] = True
if app_config.config.ENV == 'development':
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///:memory:'
else:
    app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(app_config.config.CHROMA_SERVER_PATH, "app.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

sess = Session()
api.init_app(app)
sess.init_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()

CORS(app)

@app.route('/')
def index():
    return 'received!', 200

@app.route('/health')
def health():
    return "I'm healthy", 200


if __name__ == '__main__':
    if app_config.config.ENV != 'development':
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
    else:
        app.run(debug=True)
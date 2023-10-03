from flask import Flask
from flask_session import Session
from flask_cors import CORS
from apis import api
import config as app_config

app = Flask(__name__)

app.config['SECRET_KEY']=app_config.config.SECRET_KEY
app.config['SESSION_PERMANENT'] = True
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

sess = Session()
api.init_app(app)
sess.init_app(app)
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
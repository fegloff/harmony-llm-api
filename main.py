from flask import Flask
from flask_session import Session
from flask_cors import CORS
import dotenv
from apis import api
import os

def generate_new_secret_key():
    key = os.urandom(24).hex()
    return key 

dotenv.load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY']=generate_new_secret_key()
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
    print('FCO FCO FCO ', os.getenv('FLASK_ENV'))
    if os.getenv('FLASK_ENV') != 'development':
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
    else:
        app.run(debug=True)
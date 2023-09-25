from flask import Flask, session
from flask_session import Session
from flask_cors import CORS
from res import Config
from apis import api
import os

app = Flask(__name__)

app.config.from_object(Config())

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
    app.run(debug=True)
    


from flask import Flask
from flask_cors import CORS
import dotenv
from apis import api
import os

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)
api.init_app(app)

@app.route('/')
def index():
    return 'received!', 200

@app.route('/health')
def health():
    return "I'm healthy", 200

if __name__ == '__main__': 
   app.run()
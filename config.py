from dotenv import load_dotenv, find_dotenv
import os

# env = 'development'
# if env == 'testing':
#     load_dotenv(find_dotenv('.env.testing'))
# elif env == 'development':
#     load_dotenv(find_dotenv('.env.development'))
# elif env == 'production':
#     load_dotenv(find_dotenv('.env.production'))

def generate_new_secret_key():
    key = os.urandom(24).hex()
    return key
class Config(object):
    ENV=os.environ.get('ENV') if os.environ.get('ENV') else 'production'
    DEBUG = os.environ.get('DEBUG') if os.environ.get('DEBUG') else False
    TESTING = os.getenv('TESTING') if os.environ.get('DEBUG') else False
    SECRET_KEY = generate_new_secret_key()
    CHROMA_SERVER_PATH = os.getenv('CHROMA_SERVER_PATH') if os.getenv('CHROMA_SERVER_PATH') else "/app/data/chroma"
    OPENAI_MODEL = os.getenv('OPENAI_MODEL') if os.getenv('OPENAI_MODEL') else "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS = os.getenv('OPENAI_MAX_TOKENS') if os.getenv('OPENAI_MAX_TOKENS') else 600
    WEB_CRAWLER_HTTP = os.environ.get('WEB_CRAWLER_HTTP')

config = Config()

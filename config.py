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
    ENV=os.environ.get('ENV')
    DEBUG = os.environ.get('DEBUG')
    TESTING = os.getenv('TESTING')
    SECRET_KEY = generate_new_secret_key()
    SESSION_TYPE = os.getenv('SESSION_TYPE')
    CHROMA_SERVER_PATH = os.getenv('CHROMA_SERVER_PATH')
    # CHROMA_SERVER_HOST = os.getenv('CHROMA_SERVER_HOST')
    # CHROMA_SERVER_HTTP_PORT = os.getenv('CHROMA_SERVER_HTTP_PORT')
    WEB_CRAWLER_HTTP = os.environ.get('WEB_CRAWLER_HTTP')

config = Config()




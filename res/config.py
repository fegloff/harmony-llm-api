import os

def generate_new_secret_key():
    key = os.urandom(24).hex()
    return key
class Config(object):
    DEBUG = os.getenv('DEBUG')
    TESTING = os.getenv('TESTING')
    SECRET_KEY = generate_new_secret_key()
    SESSION_TYPE = os.getenv('SESSION_TYPE')
    CHROMA_SERVER_HOST = os.getenv('CHROMA_SERVER_HOST')
    CHROMA_SERVER_HTTP_PORT = os.getenv('CHROMA_SERVER_HTTP_PORT')
    WEB_CRAWLER_HTTP = os.getenv('WEB_CRAWLER_HTTP')

config = Config()

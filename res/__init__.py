from dotenv import load_dotenv
import logging
import sys

from .text_messages import EngMsg
from .config import config

env = 'development'

if env == 'testing':
    load_dotenv('.env.testing')
elif env == 'development':
    load_dotenv('.env.development')
elif env == 'production':
    load_dotenv('.env.production')

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
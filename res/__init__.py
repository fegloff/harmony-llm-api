from dotenv import load_dotenv, find_dotenv
import logging
import sys

from .text_messages import EngMsg

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
from dotenv import load_dotenv, find_dotenv
import logging
import sys

from .text_messages import EngMsg
from .llm_exceptions import InvalidCollectionName, PdfFileInvalidFormat

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
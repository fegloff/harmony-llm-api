from flask import jsonify
from llama_index import Document, ServiceContext, SummaryIndex, VectorStoreIndex, SimpleWebPageReader, TrafilaturaWebReader
from llama_index.vector_stores import ChromaVectorStore
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from llama_index.storage.storage_context import StorageContext
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.embeddings import LangchainEmbedding
import logging
import sys
from services import BotHandler
import requests

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


class TextArray:

    def __init__(self, storage_provider):
        self.db = storage_provider

    def textQuery(self, url, prompt, bot_token, chatID, msg_id):
        try:
            enhacedPrompt = f'You will receive a web crawling text. Please get keys concepts, but try to stay within 4000 words in your response. Here is the prompt: {prompt}'
            query_engine = self.db.getQueryEngineFromUrl(chatID, url)
            promptResponse = query_engine.query(enhacedPrompt)
            bot = BotHandler(bot_token)
            bot.edit_message(str(promptResponse),chatID, msg_id)
        except Exception as e:
            error_message = str(e)
            print(f"Unexpected Error: {error_message}")
            return {
                "error": "An unexpected error occurred.",
                "error_message": error_message
            }

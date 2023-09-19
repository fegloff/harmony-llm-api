from flask import jsonify
from llama_index import Document, SummaryIndex, VectorStoreIndex, SimpleWebPageReader, TrafilaturaWebReader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
import logging
import sys
import requests
import json

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

def textQuery(textArray, prompt):
    try:
        documents = [Document(text=t) for t in textArray]
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        promtpResponse = query_engine.query(prompt)
        return str(promtpResponse)
    except Exception as e:
        error_message = str(e)
        print(f"Unexpected Error: {error_message}")
        return {
            "error": "An unexpected error occurred.",
            "error_message": error_message
        }

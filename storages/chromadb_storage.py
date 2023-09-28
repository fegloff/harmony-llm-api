
from llama_index import Document, VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
import chromadb
import hashlib

from services import WebCrawling
from res import config
class ChromaStorage:

    def __init__(self):
        self.db = chromadb.HttpClient(host=f"{config.CHROMA_SERVER_HOST}:{config.CHROMA_SERVER_HTTP_PORT}",ssl=True) #:{config.CHROMA_SERVER_HTTP_PORT}

    def get_collection_name(self, url, chat_id):
        input_string = f"{chat_id}:{url}"
        hashed = hashlib.md5(input_string.encode()).hexdigest()
        if not hashed[0].isalnum():
            hashed = 'a' + hashed[1:]
        if not hashed[-1].isalnum():
            hashed = hashed[:-1] + 'a'
        valid_characters = ''.join(c for c in hashed if c.isalnum() or c in ('_', '-'))
        return valid_characters

    def get_collection(self, chat_id, url):
        collection_name = self.get_collection_name(url,chat_id) 
        collection = self.db.get_or_create_collection(
            name=collection_name)
        return collection
    
    def get_vector_index_from_url(self, chat_id, url):
        collection = self.get_collection(chat_id, url)   
        if (collection.count() > 0):
            vector_store = ChromaVectorStore(chroma_collection=collection)
            index = VectorStoreIndex.from_vector_store(
                vector_store)
            return index
        else:
            crawl = WebCrawling()
            textArray = crawl.get_web_content(url)
            documents = [Document(text=t) for t in textArray.get('urlText')]
            vector_store = ChromaVectorStore(chroma_collection=collection)
            storage_context = StorageContext.from_defaults(
                vector_store=vector_store)
            index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context)
            return index



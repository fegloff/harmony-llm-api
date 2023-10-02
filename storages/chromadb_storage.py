
from llama_index import Document, VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
import chromadb
import hashlib

from services import WebCrawling
from res import config
class ChromaStorage:

    def __init__(self):
        self.db = chromadb.Client() # HttpClient(host=config.CHROMA_SERVER_HOST,port=config.CHROMA_SERVER_HTTP_PORT, ssl=True) #:{config.CHROMA_SERVER_HTTP_PORT}

    def get_collection_name(self, chat_id, url, pdf):
        if url:
            return self.generate_collection_name(chat_id, url)
        if pdf and pdf.get("name"):
            return self.generate_collection_name(chat_id, pdf["name"])
        return f"chat{chat_id}"

    def generate_collection_name(self, chat_id, str_input):
        hashed = hashlib.md5(str_input.encode()).hexdigest()
        if not hashed[0].isalnum():
            hashed = 'a' + hashed[1:]
        if not hashed[-1].isalnum():
            hashed = hashed[:-1] + 'a'
        valid_characters = ''.join(c for c in hashed if c.isalnum() or c in ('_', '-'))
        return f"chat{chat_id}-{valid_characters}"


    def get_collection(self, collection_name):
        collection = self.db.get_or_create_collection(
            name=collection_name)
        return collection
    
    def store_text_array_from_url(self, text_array, collection_name): 
        collection = self.get_collection(collection_name)
        documents = [Document(text=t) for t in text_array.get('urlText')]
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context)
        print(f'****** {index.summary}')
    
    def store_text_array(self, text_array, collection_name):
        collection = self.get_collection(collection_name)
        documents = [Document(text=t) for t in text_array]
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context)
        print(f'****** {index.summary}')

    def get_vector_index(self, collection_name):
        collection = self.get_collection(collection_name)
        if (collection.count() > 0):
            vector_store = ChromaVectorStore(chroma_collection=collection)
            index = VectorStoreIndex.from_vector_store(
                vector_store)
            return index
        return None
    
    # def get_vector_index_from_url(self, chat_id, url):
    #     collection = self.get_collection(chat_id, url)   
    #     if (collection.count() > 0):
    #         vector_store = ChromaVectorStore(chroma_collection=collection)
    #         index = VectorStoreIndex.from_vector_store(
    #             vector_store)
    #         return index
    #     else:
    #         crawl = WebCrawling()
    #         textArray = crawl.get_web_content(url)
    #         documents = [Document(text=t) for t in textArray.get('urlText')]
    #         vector_store = ChromaVectorStore(chroma_collection=collection)
    #         storage_context = StorageContext.from_defaults(
    #             vector_store=vector_store)
    #         index = VectorStoreIndex.from_documents(
    #             documents, storage_context=storage_context)
    #         return index



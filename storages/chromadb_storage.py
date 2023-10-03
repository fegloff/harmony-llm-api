
from llama_index import Document, VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
import chromadb
import chromadb.config
import hashlib
import os

class ChromaStorage:

    def __init__(self):
        path = '/app/data' # os.getcwd()
        # _client_settings = chromadb.config.Settings(
        #     persist_directory=f"{path}/chroma",
        #     is_persistent=True)
        self.db = chromadb.PersistentClient(f"{path}/chroma")
        
        # chromadb.Client(_client_settings) # 

    def get_collection_name(self, chat_id, url):
        hashed = hashlib.md5(url.encode()).hexdigest()
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

    def get_vector_index(self, collection_name):
        collection = self.get_collection(collection_name)
        if (collection.count() > 0):
            vector_store = ChromaVectorStore(chroma_collection=collection)
            index = VectorStoreIndex.from_vector_store(
                vector_store)
            return index
        return None
    

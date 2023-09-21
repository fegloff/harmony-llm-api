from llama_index import Document, VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
import chromadb

from services.web_crawling import WebCrawling

class ChromaStorage:

    def __init__(self):
        self.db = chromadb.PersistentClient(path="./data/chroma_db")

    def getCollection(self, chatID):
        collection_name = f'chat{chatID}'
        print(collection_name)
        collection = self.db.get_or_create_collection(
            name=collection_name)
        return collection
    
    def getQueryEngineFromUrl(self, chatID, url):
        collection = self.getCollection(chatID)   

        if (collection.count() > 0):
            vector_store = ChromaVectorStore(chroma_collection=collection)
            index = VectorStoreIndex.from_vector_store(
                vector_store)
            return index.as_query_engine()
        else:
            crawl = WebCrawling()
            textArray = crawl.get_web_content(url)
            documents = [Document(text=t) for t in textArray.get('urlText')]
            vector_store = ChromaVectorStore(chroma_collection=collection)
            storage_context = StorageContext.from_defaults(
                vector_store=vector_store)
            index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context)
            return index.as_query_engine()




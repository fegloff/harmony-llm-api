import os
import shutil

from storages import ChromaStorage
from llama_index.chat_engine.types import ChatMode
from res import InvalidCollectionName
class CollectionHelper:

    def __init__(self, storage_provider: ChromaStorage):
        self.db = storage_provider

    def get_db(self):
        return self.db
    
    def get_collection_name(self, chat_id, url):
        return self.db.get_collection_name(chat_id, url)

    def is_pdf_url(self, url):
        return url.lower().endswith('.pdf')    
    
    def get_collection(self, collection_name): 
        collection = self.db.get_collection(collection_name)
        return collection

    def collection_query(self, collection_name, prompt, conversation):
        index = self.db.get_vector_index(collection_name)
        if index:
            chat_engine = index.as_chat_engine(chat_mode=ChatMode.CONTEXT) # "condense_question")
            promptResponse = chat_engine.chat(prompt,chat_history=conversation) # chat_history=conversation
            return {
                "completion": str(promptResponse),
                "price": 0.02
            }
        else: 
            raise InvalidCollectionName("Collection Error", "collection doesn't exist, please try again later", 404)

    def delete_collection(self, collection_name):
        collection = self.db.get_existing_collection(collection_name)
        if (collection):
            self.db.delete_collection(collection_name)
            # path = self.db.get_path()
            # folder = f"{path}/{collection.id}"
            # if (os.path.isdir(folder)):
            #     shutil.rmtree(folder)
    
    def reset_database(self):
        return self.db.reset_database()
    
    # def delete_folders(self):
    #     path = self.db.get_path()
    #     contents = os.listdir(path)
    #     for item in contents:
    #         item_path = os.path.join(path, item)
    #         if os.path.isdir(item_path):
    #             shutil.rmtree(item_path, ignore_errors=True)

from storages import ChromaStorage
from services import WebCrawling

class CollectionHelper:

    def __init__(self, storage_provider: ChromaStorage):
        self.db = storage_provider

    def get_collection_name(self, chat_id, url, pdf):
        return self.db.get_collection_name(chat_id, url, pdf)
    
    def collection_request_handler(self, url, pdf, collection_name):
        if (url):
            crawl = WebCrawling()
            text_array = crawl.get_web_content(url)
            self.db.store_text_array_from_url(text_array,collection_name)
        elif (pdf):
            # TO BE DEFINED
            # documents = [Document(text=t) for t in pdfNodes]
            print('TBD pdf')

    def get_collection(self, collection_name): 
        collection = self.db.get_collection(collection_name)
        return collection

    def collection_query(self, collection_name, prompt, conversation):
        index = self.db.get_vector_index(collection_name)
        chat_engine = index.as_chat_engine(chat_mode="condense_question")
        promptResponse = chat_engine.chat(prompt)
        print(f':::::::::::: {promptResponse}')
        return str(promptResponse)
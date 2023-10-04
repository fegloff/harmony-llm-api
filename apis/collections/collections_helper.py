from storages import ChromaStorage
from llama_index.chat_engine.types import ChatMode
from services import WebCrawling, PdfHandler

class CollectionHelper:

    def __init__(self, storage_provider: ChromaStorage):
        self.db = storage_provider

    def get_collection_name(self, chat_id, url):
        return self.db.get_collection_name(chat_id, url)

    def is_pdf_url(self, url):
        return url.lower().endswith('.pdf')    
    
    def collection_request_handler(self, url, file_name, collection_name):
        if (not self.is_pdf_url(url)):
            crawl = WebCrawling()
            text_array = crawl.get_web_content(url)
            self.db.store_text_array_from_url(text_array,collection_name)
        else:
            pdf_handler = PdfHandler()
            chunks = pdf_handler.pdf_to_chunks(url)
            self.db.store_text_array(chunks, collection_name)
            # documents = [Document(text=t) for t in pdfNodes]

    def get_collection(self, collection_name): 
        collection = self.db.get_collection(collection_name)
        return collection

    def get_collection(self, collection_name): 
        collection = self.db.get_collection(collection_name)
        return collection

    def get_collection(self, collection_name): 
        collection = self.db.get_collection(collection_name)
        return collection

    def collection_query(self, collection_name, prompt, conversation):
        index = self.db.get_vector_index(collection_name)
        if index:
            chat_engine = index.as_chat_engine(chat_mode=ChatMode.CONTEXT) # "condense_question")
            # print(conversation)
            promptResponse = chat_engine.chat(prompt,chat_history=conversation) # chat_history=conversation
            return {
                "completion": str(promptResponse),
                "price": 0.02
            }
        else: 
            raise Exception("Collection Error", "collection doesn't exist, please try again later", 404)

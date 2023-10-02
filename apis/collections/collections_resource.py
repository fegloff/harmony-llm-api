from flask import request, jsonify
from flask_restx import Namespace, Resource
import json
import threading

from res import EngMsg as msg
from storages import chromadb
from .collections_helper import CollectionHelper

api = Namespace('collections', description=msg.API_NAMESPACE_LLMS_DESCRIPTION)

def data_generator(response):
    for chunk in response:
        yield f"data: {json.dumps(chunk)}\n\n"

collection_helper = CollectionHelper(chromadb)

@api.route('/document')
class AddDocument(Resource):
    def post(self):
        """
        Endpoint that creates collections
        Receives any document (URL, PDF, voice) and creates a collection (Vector index).
        Returns a collection ID
        """
        data = request.json
        chat_id = data.get('chatId')
        url = data.get('url')
        # pdf looks as follows:
        # pdf {
        #   name: "file_name.pdf"
        #   url: "file_url"
        # }
        pdf = data.get('pdf')
        try:
            if (chat_id and (url or pdf)):
                collection_name = collection_helper.get_collection_name(chat_id, url, pdf)
                thread = threading.Thread(target=collection_helper.collection_request_handler, args=(url, pdf, collection_name))
                thread.start()
                return f'{collection_name}', 200
            else:
                return "Bad request, parameters missing", 400
        except Exception as e:
            error_message = str(e)
            print(f"Unexpected Error: {error_message}")
            return jsonify({"error": "An unexpected error occurred."}), 500

    def get(self):
        """
        Endpoint that checks collection creation status.
        If collection exists, returns indexing price
        """
        try:
            data = request.json
            id = data.get('collectionName')
            if (id):
                print(f'hi TBD {id}')
                return "0", 400
            else:
                return "Bad request, parameters missing", 400    
        except Exception as e:
            error_message = str(e)
            print(f"Unexpected Error: {error_message}")
            return jsonify({"error": "An unexpected error occurred."}), 500


@api.route('/query')
class WebCrawlerTextRes(Resource):
    # 
    # @copy_current_request_context
    def post(self):
        """
        Endpoint to handle LLMs request.
        Receives a message from the user, processes it, and returns a response from the model.
        """ 
        data = request.json
        prompt = data.get('prompt')
        collection_name = data.get('collectionName')
        conversation = data.get('conversation')
        try:
            if collection_name:
                response = collection_helper.collection_query(collection_name, prompt, conversation)
                return response, 200
            else:
                return "Bad request, parameters missing", 400
        except Exception as e:
            error_message = str(e)
            print(f"Unexpected Error: {error_message}")
            return jsonify({"error": "An unexpected error occurred."}), 500
        
# @api.route('/text')
# class WebCrawlerTextRes(Resource):
#     # 
#     # @copy_current_request_context
#     def post(self):
#         """
#         Endpoint to handle LLMs request.
#         Receives a message from the user, processes it, and returns a response from the model.
#         """ 
#         data = request.json
#         prompt = data.get('prompt')
#         token = data.get('token')
#         chatId = data.get('chatId')
#         msgId = data.get('msgId')
#         url = data.get('url')
#         try:
#             if prompt and token and chatId and msgId and url:
#                 thread = threading.Thread(target=text_array.text_query, args=(url, prompt, token, chatId, msgId))
#                 thread.start()
#                 return 'OK', 200
#             else:
#                 return "Bad request, parameters missing", 400
#         except openai.error.OpenAIError as e:
#             error_message = str(e)
#             print(f"OpenAI API Error: {error_message}")
#             return jsonify({"error": error_message}), 500
#         except Exception as e:
#             error_message = str(e)
#             print(f"Unexpected Error: {error_message}")
#             return jsonify({"error": "An unexpected error occurred."}), 500        


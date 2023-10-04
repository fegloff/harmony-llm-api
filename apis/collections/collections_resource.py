from flask import request, jsonify, make_response, current_app as app
from flask_restx import Namespace, Resource
import json
import threading
from llama_index.llms.base import ChatMessage
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
        app.logger.info('handling document')
        data = request.json
        chat_id = data.get('chatId')
        url = data.get('url')
        file_name = data.get('fileName')
        try:
            if (chat_id and url):
                collection_name = collection_helper.get_collection_name(chat_id, url)
                thread = threading.Thread(target=collection_helper.collection_request_handler, args=(url, file_name, collection_name))
                thread.start()
                return make_response(jsonify({"collectionName": f"{collection_name}"}), 200)
            else:
                return make_response(jsonify({"error": "Bad request, parameters missing"}), 400)
        except Exception as e:
            error_message = str(e)
            app.logger.error(f"Unexpected Error: {error_message}")
            return make_response(jsonify({"error": "An unexpected error occurred."}), 500)

@api.route('/document/<collection_name>')
class CheckDocument(Resource):

    @api.doc(params={"collection_name": msg.API_DOC_PARAMS_COLLECTION_NAME})
    def get(self, collection_name):
        """
        Endpoint that checks collection creation status.
        If collection exists, returns indexing price
        """
        try:
            app.logger.info('Checking collection status')
            if (collection_name):
                collection = collection_helper.get_collection(collection_name)
                if (collection):
                    embeddings_number = collection.count()
                    app.logger.info(f'******* Number of embeddings: {embeddings_number}')
                    response = {
                        "price": embeddings_number * 0.05 # TBD
                    }
                    return make_response(jsonify(response), 200)
                response = {
                    "price": -1
                }
                return make_response(jsonify(response), 200)
            else:
                return "Bad request, parameters missing", 400    
        except Exception as e:
            error_message = str(e)
            app.logger.error(f"Unexpected Error: {error_message}")
            return make_response(jsonify({"error": "An unexpected error occurred."}), 500)

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
        chat_history = [ChatMessage(content=item.get('content'), role=item.get('role')) for item in conversation]
        try:
            app.logger.info('Inquiring a collection')
            if collection_name:
                response = collection_helper.collection_query(collection_name, prompt, chat_history) 
                return make_response(jsonify(response), 200)
            else:
                return make_response(jsonify({"error": "Bad request"}), 400)
        except Exception as e:
            error_message = str(e)
            app.logger.error(f"Unexpected Error: {error_message}")
            if (e.args[2] == 404):
                return e.args[1], 404
            else:
                return make_response(jsonify({"error": "An unexpected error occurred."}), 500)

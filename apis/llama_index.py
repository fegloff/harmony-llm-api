from flask import request, jsonify, session, copy_current_request_context
from flask_restx import Namespace, Resource

from litellm import completion
from embeddings import TextArray 
from res import EngMsg as msg
import openai
import json
import threading
from storages import ChromaStorage

api = Namespace('llama-index', description=msg.API_NAMESPACE_LLMS_DESCRIPTION)

def data_generator(response):
    for chunk in response:
        yield f"data: {json.dumps(chunk)}\n\n"

chromadb = ChromaStorage()
text_array = TextArray(chromadb)
@api.route('/text')
class WebCrawlerTextRes(Resource):
    # 
    # @copy_current_request_context
    def post(self):
        """
        Endpoint to handle LLMs request.
        Receives a message from the user, processes it, and returns a response from the model.
        """ 
        data = request.json
        # print(data)
        # textArray = data.get('text')
        prompt = data.get('prompt')
        token = data.get('token')
        chatId = data.get('chatId')
        msgId = data.get('msgId')
        url = data.get('url')
        print(prompt, token, chatId, msgId, url)
        try:
            if prompt and token and chatId and msgId and url:
                thread = threading.Thread(target=text_array.textQuery, args=(url, prompt, token, chatId, msgId))
                thread.start()
                # print(session.get(chatId))
                # if chatId not in session:
                #     print('way')
                #     print(chatId)
                #     session[chatId] = chatId
                #     print(f'my session {session.get(chatId)}')

                # else:
                #     print('no way jose')
                return 'OK', 200
            else:
                return "Bad request, parameters missing", 400
        except openai.error.OpenAIError as e:
            error_message = str(e)
            print(f"OpenAI API Error: {error_message}")
            return jsonify({"error": error_message}), 500
        except Exception as e:
            error_message = str(e)
            print(f"Unexpected Error: {error_message}")
            return jsonify({"error": "An unexpected error occurred."}), 500


@api.route('/test')
class LlamaTest(Resource):
    def get(self):
        fco = vector_index.getIdFromUrl("https://harmony.one/q4")
        print(f'HOLA HOLA HOLA {fco}')
        return "I'm healthy", 200

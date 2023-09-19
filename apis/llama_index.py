from flask import request, jsonify, Response
from flask_restx import Namespace, Resource

from litellm import completion 
from res import EngMsg as msg
import openai
import json

from utils.web_crawling import textQuery

api = Namespace('llama-index', description=msg.API_NAMESPACE_LLMS_DESCRIPTION)

def data_generator(response):
    for chunk in response:
        yield f"data: {json.dumps(chunk)}\n\n"

@api.route('/text')
class WebCrawlerTextRes(Resource):
    def post(self):
        """
        Endpoint to handle LLMs request.
        Receives a message from the user, processes it, and returns a response from the model.
        """ 
        data = request.json
        # print(data)
        textArray = data.get('text')
        prompt = data.get('prompt')
        try:
            if (textArray and prompt):
                response = textQuery(textArray, prompt) 
                return response, 200
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


from flask import request, jsonify, Response
from flask_restx import Namespace, Resource
from litellm import litellm, completion
from res import EngMsg as msg
import openai
import json

api = Namespace('llms', description=msg.API_NAMESPACE_LLMS_DESCRIPTION)

def data_generator(response):
    for chunk in response:
        yield f"data: {json.dumps(chunk)}\n\n"

@api.route('/completions') 
class LlmsCompletionRes(Resource):
    
    def post(self): 
        data = request.json
        if data.get('stream') == "True":
            data['stream'] = True # convert to boolean
        # if not data:

        #     return jsonify({"error": "Invalid request data"}), 400
        try:
            if data.get('stream') == "True":
                data['stream'] = True # convert to boolean
            # pass in data to completion function, unpack data
            response = completion(**data)
            if data['stream'] == True: 
                return Response(data_generator(response), mimetype='text/event-stream')
            return response, 200 
        except openai.error.OpenAIError as e:
            # Handle OpenAI API errors
            error_message = str(e)
            print(f"OpenAI API Error: {error_message}")
            return jsonify({"error": error_message}), 500
        except Exception as e:
            # Handle other unexpected errors
            error_message = str(e)
            print(f"Unexpected Error: {error_message}")
            return jsonify({"error": "An unexpected error occurred."}), 500


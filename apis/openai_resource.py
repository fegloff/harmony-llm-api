from flask import request, jsonify, make_response, current_app as app
from flask_restx import Namespace, Resource
from werkzeug.utils import secure_filename
from openai.error import OpenAIError
import openai
import os
from res import EngMsg as msg

api = Namespace('openai', description=msg.API_NAMESPACE_OPENAI_DESCRIPTION)

ALLOWED_EXTENSIONS = {'wav', 'm4a', 'mp3'}
def get_transcription(path):
  try:
      audio_file = open(path, 'rb')
      response = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file
      )
      print(response)
      return response.text 
  except Exception as e:
      print('Error:', e)
      return None

def allowed_file(filename):
      return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/upload-audio', methods=['POST'])
class UploadAudioFile(Resource):
  @api.doc(params={"data": msg.API_DOC_PARAMS_DATA})
  def post(self):
    """
    Endpoint to handle Openai's Whisper request.
    Receives an audio from the user, processes it, and returns a transcription.
    """ 
    app.logger.info('handling whisper request')
    data = request.files
    try:
      print(data)
      if 'data' not in request.files:
        return make_response(jsonify({"error": 'No file part'})), 400
      file = data['data']
      if file.filename == '':
        return make_response(jsonify({"error": 'No selected file'})), 400
      if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        app.logger.info(filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        transcription = get_transcription(file_path)
        app.logger.info(f'transcription: {transcription}')
        os.remove(file_path)
        return f"{transcription}", 200
      else:
        return make_response(jsonify({"error": 'Invalid file format'})), 400
    except OpenAIError as e:
        # Handle OpenAI API errors
        error_message = str(e)
        app.logger.error(f"OpenAI API Error: {error_message}")
        return jsonify({"error": error_message}), 500
    except Exception as e:
        # Handle other unexpected errors
        error_message = str(e)
        app.logger.error(f"Unexpected Error: {error_message}")
        return jsonify({"error": "An unexpected error occurred."}), 500


from flask import request, current_app as app
from flask_restx import Namespace, Resource
from werkzeug.utils import secure_filename
from openai.error import OpenAIError
import openai
import os

from res import EngMsg as msg

api = Namespace('openai', description=msg.API_NAMESPACE_LLMS_DESCRIPTION)

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
  def post(self):
    data = request.files
    print(data)
    if 'data' not in request.files:
        return 'No file part', 400
    file = data['data']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        print(file.content_length)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        transcription = get_transcription(file_path)
        return f"{transcription}", 200
    else:
        return 'Invalid file format', 400


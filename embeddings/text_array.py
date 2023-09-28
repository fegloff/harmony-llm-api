import logging
import sys
from services import BotHandler

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

class TextArray:

    def __init__(self, storage_provider):
        self.db = storage_provider

    def text_query(self, url, prompt, bot_token, chatID, msg_id):
        try:
            index = self.db.get_vector_index_from_url(chatID, url)
            chat_engine = index.as_chat_engine(chat_mode="condense_question")
            promptResponse = chat_engine.chat(prompt) 
            bot = BotHandler(bot_token)
            bot.edit_message(str(promptResponse),chatID, msg_id)
        except Exception as e:
            error_message = str(e)
            print(f"Unexpected Error: {error_message}")
            return {
                "error": "An unexpected error occurred.",
                "error_message": error_message
            }

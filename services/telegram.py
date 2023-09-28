import telebot

class BotHandler:
    
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def edit_message(self, msg, chat_id, message_id):
        self.bot.edit_message_text(text=msg, chat_id=chat_id, message_id=message_id)
    
    def send_message(self, msg, chat_id):
        self.bot.send_message(chat_id=chat_id, text=msg)

    def __del__(self):
      self.bot.stop_bot()

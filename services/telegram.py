import requests

def bot_send_text(bot_token, bot_chatID, msg_id, bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/editMessageText?chat_id=' + bot_chatID + '&message_id='+ msg_id + '&parse_mode=Markdown&text=' + bot_message
    print(send_text)
    response = requests.get(send_text)
    print(response)
    return response

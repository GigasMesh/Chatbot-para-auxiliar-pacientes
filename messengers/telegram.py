import requests
import json


class TelegramBot:
    def __init__(self):
        self.token = open('messengers/tokenTelegram.txt').read()
        self.url_base = f'https://api.telegram.org/bot{self.token}/'
    
    # Start Bot
    def startBot(self):
        update_id = None
        while True:
            update = self.getMessages(update_id)
            data = update["result"]
            if data:
                for item in data:
                    print(item)
                    if 'message' in item:
                        update_id = item['update_id']
                        chat_id = item["message"]["from"]["id"]
                        is_first_message = item["message"]["message_id"] == 1
                        answer = self.createAnswer(is_first_message, item)
                        self.reply(answer, chat_id)

    # Get messages from chat
    def getMessages(self, update_id):
        link_request = f'{self.url_base}getUpdates?timeout=20'
        if update_id:
            link_request = f'{link_request}&offset={update_id + 1}'
        message = requests.get(link_request)
        return json.loads(message.content)

    # Create Answer
    def createAnswer(self, is_first_message, item):
        item = item['message']['text']
        if is_first_message:
            return "Olá, seja bem-vindo ao MedBot, mande uma mensagem, e eu repetirei ela!"

        else:
            return item

    # Reply messages
    def reply(self, answer, chat_id):
        replyLink = f'{self.url_base}sendMessage?chat_id={chat_id}&text={answer}'
        requests.get(replyLink)

import requests
import time
import json

class Testebot:
    def __init__(self):
      token = '1958854132:AAF8FTfPLkRSc2_u8AkjdtEKyqwLQO3URbs'
      self.url_base = f'https://api.telegram.org/bot{token}/'
    #Iniciar o bot
    def startBot(self):
      update_id = None
      while True:
        update = self.getMessages(update_id)
        data = update["result"]
        if data: 
          for item in data:
            update_id = item['update_id']
            chat_id = item["message"]["from"]["id"]
            answer = self.createAnswer()
            self.reply(answer, chat_id)

    #Obter mensagens
    def getMessages(self, update_id):
      link_request = f'{self.url_base}getUpdates?timeout=20'
      if update_id:
        link_request = f'{link_request}&offset={update_id + 1}'
      message = requests.get(link_request)
      return json.loads(message.content)
    #Criar Respostas 
    def createAnswer(self):
      return 'Só quero que me diga, qual o papo? '
    #responder mensagens 
    def reply(self, answer, chat_id):
      replyLink = f'{self.url_base}sendMessage?chat_id={chat_id}&text={answer}'
      requests.get(replyLink)
      
      
bot = Testebot()
bot.startBot()

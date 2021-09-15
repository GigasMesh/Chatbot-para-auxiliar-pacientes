import requests
import time

#Processo de leitura de mensagens: 
while True:
  token = '1958854132:AAF8FTfPLkRSc2_u8AkjdtEKyqwLQO3URbs'
  url_base = f'https://api.telegram.org/bot{token}/getUpdates'
  mensagem = requests.get(url_base)
  print(resultado.json())
  time.sleep(10)
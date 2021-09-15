import requests
import json


class Telegram_Bot:
    def __init__(self):
        self.token = open('token_telegram.txt').read()
        self.url_base = f'https://api.telegram.org/bot{self.token}/'

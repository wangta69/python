import os
import telegram
from dotenv import load_dotenv
# pip install python-telegram-bot
class Telegram():

    def __init__(self):
        super().__init__()

        # .env
        # TELEGRAM_BOT_TOKEN=18142740000:AAFpsaRHTIngkZskLwXwTCuXYBBBBBBBB
        # TELEGRAM_BOT_CHAT_ID=1000000021
        load_dotenv()
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_BOT_CHAT_ID')
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    def send_message(self, message):
        self.bot.sendMessage(chat_id=self.chat_id, text=message)
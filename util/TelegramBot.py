import logging

import telegram

from util.Constant import *


class TelegramBot:

    @classmethod
    def send_test_message(cls, msg: str):
        try:
            telegram_notify = telegram.Bot(TELEGRAM_TOKEN)

            telegram_notify.send_message(chat_id=TELEGRAM_CHAT_ID, text=COMPUTER_NAME + " - " + msg,
                                         parse_mode='Markdown')
        except Exception as ex:
            logging.error(ex)

    @classmethod
    def send_photo_message(cls, msg: str, photo: str):
        try:
            telegram_notify = telegram.Bot(TELEGRAM_TOKEN)
            telegram_notify.send_photo(chat_id=TELEGRAM_CHAT_ID, caption=COMPUTER_NAME + " - " + msg,
                                       photo=open(photo, "rb"), timeout=100)
        except Exception as ex:
            logging.error(ex)

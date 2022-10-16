from auth import token
import telebot
from telebot import types, TeleBot
import uuid
import os
from speech_to_text import get_text


def get_telegram_bot(token: str) -> TeleBot:
    bot: TeleBot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        intro_msg: str = "Hi! I'm Stutter helper bot. " \
                   "\nI help people with stutter to convert voice messegae to nice looking text!"
        bot.send_message(message.chat.id, intro_msg)
        bot.send_message(message.chat.id, "Please, send voice message")

    @bot.message_handler(content_types=['voice'])
    def voice_processing(message):
        filename = str(uuid.uuid4())
        file_name_full = "unconv/" + filename + ".ogg"
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name_full, 'wb') as new_file:
            new_file.write(downloaded_file)
        text: str = get_text(file_name_full)
        bot.reply_to(message, text)
        os.remove(file_name_full)

    @bot.message_handler(content_types=['text'])
    def message_text_replier(message):
        err_msg: str = "I don't understand text \nI can recognize voice only."
        bot.send_message(message.chat.id, err_msg)

    bot.polling()


if __name__ == '__main__':
    get_telegram_bot(token)

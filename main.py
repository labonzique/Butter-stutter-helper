from auth import token
import telebot
from telebot import TeleBot
from speech_to_text import get_text


def get_telegram_bot(token: str) -> None:
    bot: TeleBot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        intro_msg: str = "Hi! I'm Stutter helper bot. " \
                   "\nI help people with stutter to convert voice message to nice looking text!"
        bot.send_message(message.chat.id, intro_msg)
        bot.send_message(message.chat.id, "Please, send voice message")

    @bot.message_handler(content_types=['voice'])
    def voice_processing(message):
        fid = bot.get_file(message.voice.file_id)
        audio_file = bot.download_file(fid.file_path)
        text: str = get_text(audio_file)
        bot.reply_to(message, text)

    @bot.message_handler(content_types=['text'])
    def message_text_replier(message):
        err_msg: str = "I don't understand text \nI can recognize voice only."
        bot.send_message(message.chat.id, err_msg)

    bot.polling()


if __name__ == '__main__':
    get_telegram_bot(token)

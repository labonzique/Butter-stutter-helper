import requests
from datetime import datetime
from auth import token
import telebot
from telebot import types
# import bot_manager as bm
import uuid
import os
import speech_recognition  as sr
from pydub import AudioSegment
# AudioSegment.converter = os.getcwd() + "\\ffmpeg\\bin\\ffmpeg.exe"
# AudioSegment.ffmpeg = os.getcwd() + "\\ffmpeg\\bin\\ffmpeg.exe"
# AudioSegment.ffprobe = os.getcwd() + "\\ffmpeg\\bin\\ffprobe.exe"



def telegram_bot(token):
    bot = telebot.TeleBot(token)
    r = sr.Recognizer()
    language = 'en_EN'


# that is a test func, u need to paste Nadav`s func here
    def recognise(filename):
        with sr.AudioFile(filename) as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text, language=language)
                print('Converting audio transcripts into text ...')
                print(text)
                return text
            except:
                print('Sorry.. run again...')
                return "Sorry.. run again..."




    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, "Hi! I'm Stutter helper bot. \nI help people with stutter to convert voice messegae to nice looking text!",
                         # reply_markup=markup
                         )
        bot.send_message(message.chat.id, "Please, send voice message")
        # if bm.check_user(message):
        #     pass
        # else:
        #     bm.add_new_user(message)



    @bot.message_handler(content_types=['voice'])
    def voice_processing(message):
        filename = str(uuid.uuid4())
        file_name_full = "./unconv/" + filename + ".ogg"
        file_name_full_converted = "./conv/" + filename + ".wav"
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name_full, 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system("ffmpeg -i " + file_name_full + " " + file_name_full_converted)
        text = recognise(file_name_full_converted)
        bot.reply_to(message, text)
        os.remove(file_name_full)
        os.remove(file_name_full_converted)


    # import requests
    # url = "https://whisper2.lablab.ai/asr/"
    # payload = {}
    # files = [
    #     ('audio_file', ('file', open('/path/to/file', 'rb'), 'application/octet-stream'))
    # ]
    # headers = {}
    # response = requests.request("POST", url, headers=headers, data=payload, files=files)
    # print(response.text)


    @bot.message_handler(content_types=['text'])
    def message_text_replier(message):
        bot.send_message(message.chat.id,
                         "I don't understand text \nI can recognize voice only."
                         )


    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)

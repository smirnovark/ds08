import os
import urllib3
import telebot
from dotenv import load_dotenv
from weather import Weather

load_dotenv()
urllib3.disable_warnings()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler()
def get_city(message):
    bot.send_message(message.chat.id, 'Введи город')
    bot.register_next_step_handler(message, get_weather)


def get_weather(message):
    weather = Weather()
    user_weather = weather.get_weather(message.text)
    bot.send_message(message.chat.id, f'{user_weather}')

    bot.send_message(message.chat.id, 'Введи еще город')
    bot.register_next_step_handler(message, get_weather)


bot.polling(none_stop=True)

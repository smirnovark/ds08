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
    bot.send_message(message.chat.id, 'Введите город')
    bot.register_next_step_handler(message, get_weather)


def get_weather(message):
    weather = Weather()
    user_weather = weather.get_weather(message.text)
    bot.send_message(message.chat.id,
                     f'Температура воздуха: {user_weather[0]}°С\n'
                     f'Ощущается как: {user_weather[1]}°С\n'
                     f'{user_weather[2]}\n'
                     f'Атмосферное давление: {user_weather[3]}мм\n'
                     f'Влажность воздуха: {user_weather[4]}%\n'
                     f'Ветер: {user_weather[5]}, {user_weather[6]}м/с\n')

    bot.send_message(message.chat.id, 'Введите еще город')
    bot.register_next_step_handler(message, get_weather)


bot.polling(none_stop=True)

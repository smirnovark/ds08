import telebot

bot = telebot.TeleBot('5616111986:AAFDKoNTG2hig-q-JtuF7mEjoPt-kNI2BNI')

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет')

@bot.message_handler()
def get_city(message):
    bot.send_message(message.chat.id, 'Введите город')
    bot.register_next_step_handler(message, get_weather)

def get_weather(message):
    city = message.text
    bot.send_message(message.chat.id, f'{city} город герой!')

bot.polling(none_stop=True)
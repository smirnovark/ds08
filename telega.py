import telebot
import requests
import json
import geopy
import urllib3

urllib3.disable_warnings()

class weath:
    def __init__(self, city):
        self.city = city

    def get_weather(self):
        geolocator = geopy.geocoders.Nominatim(user_agent="telebot")
        latitude = float(geolocator.geocode(self.city).latitude)
        longitude = float(geolocator.geocode(self.city).longitude)
        url = f'https://api.weather.yandex.ru/v2/forecast/?lat={latitude}&lon={longitude}'
        headers = {'X-Yandex-API-Key': 'cfc1d734-25f1-4b4e-8f0b-d5225d8eff00'}
        conditions = {'clear': 'Ясно', 'partly-cloudy': 'Малооблачно', 'cloudy': 'Облачно с прояснениями',
                      'overcast': 'Пасмурно', 'drizzle': 'Морось', 'light-rain': 'Небольшой дождь',
                      'rain': 'Дождь', 'moderate-rain': 'Умеренно сильный', 'heavy-rain': 'Сильный дождь',
                      'continuous-heavy-rain': 'Длительный сильный дождь', 'showers': 'Ливень',
                      'wet-snow': 'Дождь со снегом', 'light-snow': 'Небольшой снег', 'snow': 'Снег',
                      'snow-showers': 'Снегопад', 'hail': 'Град', 'thunderstorm': 'Гроза',
                      'thunderstorm-with-rain': 'Дождь с грозой', 'thunderstorm-with-hail': 'Гроза с градом'
                      }
        wind_dir = {'nw': 'северо-западный', 'n': 'северный', 'ne': 'северо-восточный', 'e': 'восточный',
                    'se': 'юго-восточный', 's': 'южный', 'sw': 'юго-западный', 'w': 'западный', 'с': 'штиль'}
        r = requests.get(url=url, headers=headers)
        data = json.loads(r.text)
        data['fact']['condition'] = conditions[data['fact']['condition']]
        data['fact']['wind_dir'] = wind_dir[data['fact']['wind_dir']]

        return data['fact']['temp'], data['fact']['feels_like'], data['fact']['condition'], data['fact']['pressure_mm'], data['fact']['humidity'], data['fact']['wind_dir'], data['fact']['wind_speed']

bot = telebot.TeleBot('5616111986:AAFDKoNTG2hig-q-JtuF7mEjoPt-kNI2BNI')

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет')

@bot.message_handler()
def get_city(message):
    bot.send_message(message.chat.id, 'Введите город')
    bot.register_next_step_handler(message, get_weather)

def get_weather(message):
    weather = weath(message.text)
    user_weather = weather.get_weather()
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
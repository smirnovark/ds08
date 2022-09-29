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
        conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                      'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                      'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                      'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                      'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                      'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                      'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                      }
        wind_dir = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное',
                    'se': 'юго-восточное', 's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'с': 'штиль'}
        r = requests.get(url=url, headers=headers)
        data = json.loads(r.text)
        #fact = data['fact']
        data['fact']['condition'] = conditions[data['fact']['condition']]
        data['fact']['wind_dir'] = wind_dir[data['fact']['wind_dir']]

        return data['fact']['temp'], data['fact']['feels_like'], data['fact']['condition'], data['fact']['pressure_mm'], data['fact']['humidity'], data['fact']['wind_dir'], data['fact']['wind_speed']

weather = weath('Москва')


user_weather = weather.get_weather()
print(user_weather)






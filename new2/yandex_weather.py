# coding=utf-8
import os
import json
import urllib3
import requests
from typing import Dict
import geopy
from dotenv import load_dotenv
from attrs import define
from config import CONDITION2RU, WIND2RU

load_dotenv()
urllib3.disable_warnings()


class YandexWeather:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_yandex_weather(self, city: str) -> Dict:
        geolocator = geopy.geocoders.Nominatim(user_agent="telebot")
        latitude = float(geolocator.geocode(city).latitude)
        longitude = float(geolocator.geocode(city).longitude)
        url = f'https://api.weather.yandex.ru/v2/forecast/?lat={latitude}&lon={longitude}'
        headers = {'X-Yandex-API-Key': self.api_key}
        r = requests.get(url=url, headers=headers)
        data = json.loads(r.text)
        data['fact']['condition'] = CONDITION2RU[data['fact']['condition']]
        data['fact']['wind_dir'] = WIND2RU[data['fact']['wind_dir']]
        result = {'temp': data['fact']['temp'],
                'feels_like': data['fact']['feels_like'],
                'condition': data['fact']['condition'],
                'pressure_mm': data['fact']['pressure_mm'],
                'humidity': data['fact']['humidity'],
                'wind_dir': data['fact']['wind_dir'],
                'wind_speed': data['fact']['wind_speed']}
        return result


@define
class Weather:
    def get_weather(self, massage):
        y_weather = YandexWeather(os.getenv("YANDEX_KEY"))
        weather = y_weather.get_yandex_weather(massage)
        mess = (f"Температура воздуха: {weather['temp']}°C\n"
                f"Ощущается как: {weather['feels_like']}°C\n"
                f"{weather['condition']}\n"
                f"Атмосферное давление: {weather['pressure_mm']}мм\n"
                f"Влажность воздуха: {weather['humidity']}%\n"
                f"Ветер: {weather['wind_dir']}, {weather['wind_speed']}м/с\n")
        return mess



if __name__ == '__main__':
    message = 'Санкт-Петербург'
    user_weather = Weather()
    print(user_weather.get_weather(message))

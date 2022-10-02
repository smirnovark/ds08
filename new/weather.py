# coding=utf-8
import os
import json
import urllib3
import requests
from typing import Dict

import geopy
from dotenv import load_dotenv

from config import CONDITION2RU, WIND2RU

load_dotenv()
urllib3.disable_warnings()


class Weather:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_weather(self, city: str) -> Dict:
        geolocator = geopy.geocoders.Nominatim(user_agent="telebot")
        latitude = float(geolocator.geocode(city).latitude)
        longitude = float(geolocator.geocode(city).longitude)
        url = f'https://api.weather.yandex.ru/v2/forecast/?lat={latitude}&lon={longitude}'
        headers = {'X-Yandex-API-Key': self.api_key}
        r = requests.get(url=url, headers=headers)
        data = json.loads(r.text)
        data['fact']['condition'] = CONDITION2RU[data['fact']['condition']]
        data['fact']['wind_dir'] = WIND2RU[data['fact']['wind_dir']]

        ## TODO Сделайте здесь возвращение dict
        return data['fact']['temp'], data['fact']['feels_like'], data['fact']['condition'], data['fact']['pressure_mm'], \
               data['fact']['humidity'], data['fact']['wind_dir'], data['fact']['wind_speed']


if __name__ == '__main__':
    weather = Weather(os.getenv("YANDEX_KEY"))
    user_weather = weather.get_weather('Москва')
    print(user_weather)
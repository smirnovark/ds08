# coding=utf-8
import os
import urllib3
from yandex_weather import YandexWeather
from dotenv import load_dotenv
from attrs import define

load_dotenv()
urllib3.disable_warnings()

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
    weath = Weather(os.getenv("YANDEX_KEY"))

    message = 'Москва'
    w = weath.get_weather
    print(w)




import requests
import json
from config import API_KEY, TEMP
from template.index import main 


class WeatherShow:

    def getWeatherData(self, coords) -> dict:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={coords}&days=2&aqi=no&alerts=no"
        weatherData = requests.get(url, params={'units': 'metric', 'lang': 'ru'}).json()
        
        return weatherData
    
    def getWeather(self, coord):
        dt = self.getWeatherData( coord )
        print(dt)
        return main(TEMP, dt)
        
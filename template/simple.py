
def weather(weatherData):
    weatherCity =  weatherData['location']['name']
    weatherCoord =  (weatherData['location']['lat'], weatherData['location']['lon'])

    
    weatherCur = weatherData['current']
    weatherCurTemp = weatherCur['temp_c']
    weatherCurCond = weatherCur['condition']['text']
    weatherCurWindDir = weatherCur['wind_dir']
    weatherCurWindKm = weatherCur['wind_kph']
    weatherCurFellsFile = weatherCur['feelslike_c']
    
    #next day
    
    weatherFor = weatherData['forecast']['forecastday'][1]['day']
    weatherForTempAV = weatherFor['avgtemp_c']
    weatherForMaxWind = weatherFor['maxwind_kph']
    
    text=f'''
    сегодня
    город {weatherCity} координаты {weatherCoord}
    текушая темпиратура {weatherCurTemp}
    скорость ветра {weatherCurWindKm}
    напрвление ветра {weatherCurWindDir}
    условия {weatherCurCond}
    ощущается как {weatherCurFellsFile}
    -------------
    завтра
    средняя темпиратура {weatherForTempAV}
    средня скорость ветра {weatherForMaxWind}
    '''
    return text
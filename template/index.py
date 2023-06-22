
def main(TEMP: str, weatherData):
    from importlib import import_module
    weath = import_module(f'template.{TEMP}')
    return weath.weather(weatherData)

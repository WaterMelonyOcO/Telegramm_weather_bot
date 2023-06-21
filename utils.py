
def getMesCom(mes: str, com: str = ''):

    try:
        if ( len(com.strip()) <= 0):
            city = mes.strip()
        else:
            city = mes.split(com)[1].strip()
        print (city)
        return city
    except:
        return mes

def getCityData(city: str) -> dict:
    import requests
    print( city)
    try:
        data = requests.get(f"https://nominatim.openstreetmap.org/?addressdetails=1&q={city}&format=json&limit=1").json()[0]
    except IndexError:
        return None
    coord = '{:.3f},{:.3f}'.format(float(data['lat']), float(data['lon']))
    displayName = data['display_name'].split(',')[0]
    return (coord, displayName)

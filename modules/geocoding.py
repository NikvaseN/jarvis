import requests

def get_coordinates(city=""):
    """
    Получает координаты по названию города.
    Если город не указан или не найден — возвращает None.
    """
    city = city.strip()
    
    if not city:
        print("[Geo] Город не указан в настройках")
        return None, None
    
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ru"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            lat = result['latitude']
            lon = result['longitude']
            return lat, lon
        
        print(f"[Geo] Город '{city}' не найден")
        return None, None
        
    except Exception as e:
        print(f"[Geo] Ошибка геокодирования: {e}")
        return None, None
from datetime import datetime
<<<<<<< Updated upstream
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from config import CITY
from tts import va_speak

def get_time_by_city():
    """
    Принимает название города и возвращает время в формате:
    'Сейчас 8 часов 30 минут вечера'
    """
    city_name = CITY
    # Находим координаты города
    geolocator = Nominatim(user_agent="time_app")
    location = geolocator.geocode(city_name)
    
    if not location:
        return f"Город '{city_name}' не найден"
    
    # Определяем часовой пояс по координатам
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    
    # Получаем время в этом часовом поясе
    tz = pytz.timezone(timezone_str)
    now = datetime.now(tz)
    
    hours = now.hour
    minutes = now.minute
    
    # Определяем время суток
    if 5 <= hours < 12:
        time_of_day = "утра"
        display_hours = hours
    elif 12 <= hours < 17:
        time_of_day = "дня"
        display_hours = hours if hours == 12 else hours - 12
    elif 17 <= hours < 23:
        time_of_day = "вечера"
        display_hours = hours - 12
    else:
        time_of_day = "ночи"
        display_hours = hours if hours == 0 else hours - 12 if hours > 12 else hours
    
    va_speak(f"Сейчас {display_hours} часов {minutes} минут {time_of_day}")
=======
from tts import va_speak

def tell_time():
    h, m = datetime.now().hour, datetime.now().minute
    
    # Время суток
    if 5 <= h < 12:   tod = "утра"
    elif 12 <= h < 17: tod = "дня"
    elif 17 <= h < 23: tod = "вечера"
    else:              tod = "ночи"
    
    # 12-часовой формат
    dh = h % 12 or 12
    
    if m == 0:
        text = f"Сейчас {dh} часов {tod}"
    else:
        text = f"Сейчас {dh} часов {m} минут {tod}"
    
    va_speak(text)
>>>>>>> Stashed changes

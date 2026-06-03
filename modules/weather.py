import requests
import re
from datetime import datetime, timedelta
from config import CITY
from modules.functions import sound
from modules.geocoding import get_coordinates
from tts import va_speak

DAYS_OF_WEEK = {
    'понедельник': 0, 'вторник': 1, 'среда': 2, 'среду': 2,
    'четверг': 3, 'пятница': 4, 'пятницу': 4,
    'суббота': 5, 'субботу': 5, 'воскресенье': 6
}

MONTHS = {
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
    'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
    'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
}


def weather(command_text=""):
    lat, lon = get_coordinates(CITY)
    
    if lat is None:
        va_speak("Город не настроен. Укажите город в файле конфигурации")
        return
    
    target_day, day_display_name = parse_day_from_command(command_text)
    
    if target_day is None:
        va_speak("Я могу показать погоду на сегодня, завтра, или на конкретный день в пределах недели")
        return
    
    if target_day < 0 or target_day > 6:
        va_speak("Прогноз доступен только на ближайшие семь дней")
        return
    
    sound('Сейчас_узнаю.mp3')
    
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,weather_code,wind_speed_10m,uv_index"
        f"&hourly=precipitation_probability"
        f"&daily=temperature_2m_max,temperature_2m_min,weather_code,uv_index_max,wind_speed_10m_mean"
        f"&timezone=auto"
    )
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        va_speak("Сервер погоды не отвечает")
        return
    except Exception as e:
        print(f"Ошибка погоды: {e}")
        va_speak("Не могу узнать погоду")
        return
    
    daily = data['daily']
    
    if target_day >= len(daily['time']):
        va_speak("Прогноз на этот день пока недоступен")
        return
    
    temp_max = daily['temperature_2m_max'][target_day]
    temp_min = daily['temperature_2m_min'][target_day]
    weather_code = daily['weather_code'][target_day]
    uv_index = daily['uv_index_max'][target_day]
    
    hourly = data['hourly']
    start_hour = target_day * 24
    end_hour = start_hour + 24
    precip_probs = hourly['precipitation_probability'][start_hour:end_hour]
    max_precip = max(precip_probs) if precip_probs else 0
    
    text_parts = []
    
    if target_day == 0:
        current = data['current']
        temp = current['temperature_2m']
        feels_like = current['apparent_temperature']
        uv_index_current = current['uv_index']
        current_weather_code = current['weather_code']
        
        wind_speed = current['wind_speed_10m'] * 0.75 * 0.65
        
        text_parts.append(f"Прогноз погоды на {day_display_name}")
        
        temp_text = format_temperature(temp)
        text_parts.append(f"сейчас за окном {temp_text}")
        
        feels_rounded = round(feels_like)
        temp_rounded = round(temp)
        if abs(feels_rounded - temp_rounded) >= 2:
            feels_text = format_temperature(feels_like)
            text_parts.append(f"по ощущениям {feels_text}")
        
        wind_text = format_wind(wind_speed).lower()
        weather_text = get_weather_description(current_weather_code)
        
        if wind_text == "штиль":
            wind_part = "ветра почти нет"
        else:
            wind_part = f"дует {wind_text} со скоростью {wind_speed:.0f} метров в секунду"
        
        text_parts.append(f"на небе {weather_text}, {wind_part}")
        
        uv_level = round(uv_index_current)
        uv_comment = get_uv_comment(uv_level)
        text_parts.append(f"ультрафиолетовый индекс сейчас {uv_level} — {uv_comment}")
        
        max_temp_text = format_temperature(temp_max)
        text_parts.append(f"днём воздух прогреется до {max_temp_text}")
        
        rain_text = format_rain_forecast(max_precip)
        text_parts.append(rain_text)
        
    else:
        wind_speed = daily['wind_speed_10m_mean'][target_day] * 0.75 * 0.65
        
        if target_day == 1:
            text_parts.append(f"Завтра ожидается")
        elif target_day == 2:
            text_parts.append(f"Послезавтра ожидается")
        elif "апреля" in day_display_name or "мая" in day_display_name:
            text_parts.append(f"На {day_display_name} планируется")
        else:
            text_parts.append(f"В {day_display_name} ожидается")
        
        weather_text = get_weather_description(weather_code)
        text_parts.append(weather_text)
        
        max_temp_text = format_temperature(temp_max)
        min_temp_text = format_temperature(temp_min).replace("плюс ", "").replace("минус ", "")
        text_parts.append(f"температура от {min_temp_text} до {max_temp_text}")
        
        wind_text = format_wind(wind_speed).lower()
        if wind_text == "штиль":
            text_parts.append("ветра почти не ожидается")
        else:
            text_parts.append(f"ожидается {wind_text} со скоростью {wind_speed:.0f} метров в секунду")
        
        uv_level = round(uv_index)
        uv_comment = get_uv_comment(uv_level)
        text_parts.append(f"ультрафиолетовый индекс {uv_level} — {uv_comment}")
        
        rain_text = format_rain_forecast(max_precip)
        text_parts.append(rain_text)
    
    full_text = ". ".join(text_parts) + "."
    va_speak(full_text)


def parse_day_from_command(text):
    """
    Определяет смещение дня и его отображаемое имя.
    Принимает строку или список слов.
    """
    if text is None:
        text = ""
    elif isinstance(text, (list, tuple)):
        text = " ".join(str(item) for item in text)
    elif not isinstance(text, str):
        text = str(text)
    
    text = text.lower()
    
    if not text or 'сегодня' in text:
        return 0, "сегодня"
    
    if 'завтра' in text:
        return 1, "завтра"
    
    if 'послезавтра' in text:
        return 2, "послезавтра"
    
    for day_name, day_index in DAYS_OF_WEEK.items():
        if day_name in text:
            today = datetime.now()
            target_weekday = day_index
            current_weekday = today.weekday()
            
            if target_weekday >= current_weekday:
                days_ahead = target_weekday - current_weekday
            else:
                days_ahead = 7 - current_weekday + target_weekday
            
            if days_ahead == 0:
                display = "сегодня"
            elif days_ahead == 1:
                display = "завтра"
            elif days_ahead == 2:
                display = "послезавтра"
            else:
                target_date = today + timedelta(days=days_ahead)
                display = f"{get_weekday_name(target_weekday)} {target_date.day} {get_month_name(target_date.month)}"
            
            return days_ahead, display
    
    date_pattern = r'(\d{1,2})\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)'
    match = re.search(date_pattern, text)
    if match:
        day = int(match.group(1))
        month_name = match.group(2)
        month = MONTHS.get(month_name)
        
        if month:
            today = datetime.now()
            target_date = datetime(today.year, month, day)
            
            if target_date.date() < today.date():
                target_date = datetime(today.year + 1, month, day)
            
            days_diff = (target_date.date() - today.date()).days
            
            if days_diff > 6:
                return -1, ""
            
            display = f"{day} {month_name}"
            return days_diff, display
    
    return 0, "сегодня"


def get_weekday_name(weekday):
    """Возвращает название дня недели"""
    days = ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье"]
    return days[weekday]


def get_month_name(month_num):
    """Возвращает название месяца в родительном падеже"""
    months = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля",
        5: "мая", 6: "июня", 7: "июля", 8: "августа",
        9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }
    return months.get(month_num, "")


def get_uv_comment(level):
    """Возвращает комментарий по уровню УФ-индекса"""
    if level <= 2:
        return "низкий"
    elif level <= 5:
        return "умеренный"
    elif level <= 7:
        return "высокий"
    elif level <= 10:
        return "очень высокий"
    else:
        return "экстремальный"


def format_temperature(temp):
    """Форматирует температуру для озвучки"""
    temp = round(temp)
    if temp > 0:
        return f"плюс {temp} {decline_degrees(temp)}"
    elif temp < 0:
        return f"минус {abs(temp)} {decline_degrees(abs(temp))}"
    else:
        return f"ноль {decline_degrees(0)}"


def decline_degrees(n):
    """Склоняет слово 'градус'"""
    n = abs(n)
    if n % 10 == 1 and n % 100 != 11:
        return "градус"
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        return "градуса"
    else:
        return "градусов"


def format_wind(speed):
    """Определяет характер ветра по скорости"""
    if speed < 1:
        return "штиль"
    elif speed < 5:
        return "слабый ветер"
    elif speed < 10:
        return "умеренный ветер"
    elif speed < 15:
        return "сильный ветер"
    else:
        return "очень сильный ветер"


def get_weather_description(code):
    """Возвращает текстовое описание погоды по коду WMO"""
    codes = {
        0: "ясно",
        1: "преимущественно ясно",
        2: "переменная облачность",
        3: "пасмурно",
        45: "туман",
        48: "изморозь",
        51: "морось",
        53: "умеренная морось",
        55: "сильная морось",
        56: "ледяная морось",
        57: "сильная ледяная морось",
        61: "небольшой дождь",
        63: "умеренный дождь",
        65: "сильный дождь",
        66: "ледяной дождь",
        67: "сильный ледяной дождь",
        71: "небольшой снег",
        73: "умеренный снег",
        75: "сильный снег",
        77: "снежные зерна",
        80: "ливень",
        81: "умеренный ливень",
        82: "сильный ливень",
        85: "снегопад",
        86: "сильный снегопад",
        95: "гроза",
        96: "гроза с градом",
        99: "сильная гроза с градом",
    }
    return codes.get(code, "непонятная погода")


def format_rain_forecast(max_probability):
    """Формирует прогноз осадков на основе максимальной вероятности за сутки"""
    if max_probability < 20:
        return "осадков не ожидается"
    elif max_probability < 50:
        return "возможен небольшой дождь"
    elif max_probability < 80:
        return "ожидается дождь"
    else:
        return "будет дождливо"
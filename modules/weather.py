from dotenv import load_dotenv
import os
from modules.parser import parse
from modules.functions import sound
from tts import va_speak
load_dotenv()

def soupGetTemp(soup, name):
    weather_div = soup.select(f"div.{name}")[0]
    temperature_element = weather_div.find("span", class_="unit_temperature_c")
    if(temperature_element):
        sign = temperature_element.find("span", class_="sign")
        try:
            sign = sign.contents[-1].strip()
        except:
            sign = ''
        temp = temperature_element.contents[-1].strip()
        return f'{sign}{temp}'

def getWind(soup):
    info = soup.select('div.now-info')[0]
    wind_text = info.find("div", class_="unit_wind_km_h").text.strip()
    wind_digits = ''.join(filter(str.isdigit, wind_text))
    return wind_digits

def getHumidity(soup):
    info = soup.select('div.now-info-item.humidity')[0]
    humidity = info.find("div", class_="item-value").text.strip()
    return humidity

def print_percentage(n):
    n = int(n)
    if n % 10 == 1 and n % 100 != 11:
        return "процент"
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        return "процента"
    else:
        return "процентов"

def weather():
    sound('Сейчас_узнаю.mp3')
    HOST = os.getenv("WEATHER_URL")
    soup = parse(HOST)
    now_weather = soupGetTemp(soup, 'now-weather')
    now_feel = soupGetTemp(soup, 'now-feel')
    now_desc = soup.find("div", class_="now-desc").text.strip()
    now_wind = getWind(soup)
    now_humidity = getHumidity(soup)
    text = f"Погода сейчас {now_weather}, По ощущениям {now_feel}, {now_desc}. Ветер {now_wind} км в час. Влажность {now_humidity} {print_percentage(now_humidity)}."
    print(text)
    va_speak(text)
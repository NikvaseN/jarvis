from dotenv import load_dotenv
import os
from modules.parser import parse
from modules.functions import sound
from tts import va_speak
load_dotenv()

# def print_percentage(n):
#     n = int(n)
#     if n % 10 == 1 and n % 100 != 11:
#         return "процент"
#     elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
#         return "процента"
#     else:
#         return "процентов"

def weather():
    sound('Сейчас_узнаю.mp3')
    HOST = os.getenv("WEATHER_URL")
    soup = parse(HOST)

    # selected = soup.select(f"div.AppFact_wrap_withReport__HYdAy")[0]
    now_status = soup.find("p", class_="AppFact_warning__8kUUn").text.strip()
    now_temp_sign = soup.find("span", class_="AppFactTemperature_sign__1MeN4").text.strip()
    now_temp_value = soup.find("span", class_="AppFactTemperature_value__2qhsG").text.strip()
    now_temp_feels = soup.find("span", class_="AppFact_feels__IJoel AppFact_feels_withYesterday__yE440").text.strip('°')
    today_select = soup.select(f"div.AppShortForecastDay_container__r4hyT")[0]
    today_temp_max = today_select.find("span", class_="AppShortForecastDay_temperature__DV3oM").text.strip('°')
    now_uf_index = soup.find("span", class_="UvIndexRange_range__number__KkOdl").text.strip()

    text = f"На улице {now_status}, Сейчас температура {now_temp_sign + now_temp_value}°, {now_temp_feels}, Максимальная температура {today_temp_max}, УФ индекс {now_uf_index}."
    va_speak(text)
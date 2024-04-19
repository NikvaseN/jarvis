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

def weather():
	sound('Сейчас_узнаю.mp3')
	HOST = os.getenv("WEATHER_URL")
	soup = parse(HOST)
	now_weather = soupGetTemp(soup, 'now-weather')
	now_feel = soupGetTemp(soup, 'now-feel')
	now_desc = soup.find("div", class_="now-desc").text.strip()
	text = f"Погода сейчас {now_weather} и {now_feel} по ощущениям, {now_desc}"
	print(text)
	va_speak(text)
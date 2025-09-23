from openai import OpenAI
from dotenv import load_dotenv
import os
from modules.functions import remove_smileys
from modules.functions import sound
from tts import va_speak
import requests
import time
import uuid

load_dotenv()

API_KEY_GPT = os.getenv("API_KEY_GPT")

def sendQuest(text):
    try:
        sound('Сейчас_узнаю.mp3')
        text_str = ' '.join(text)
        
        client = OpenAI(
			api_key=API_KEY_GPT,
			base_url="https://api.laozhang.ai/v1"
		)
        
        completion = client.chat.completions.create(
			model="gpt-4o",
			messages=[
				{"role": "system", "content": "Ты полезный помощник. Отвечай кратко на русском."},
				{"role": "user", "content": text_str}
			]
		)
        response = completion.choices[0].message.content
        print(response)
        va_speak(response)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        va_speak("Не удалось получить ответ")






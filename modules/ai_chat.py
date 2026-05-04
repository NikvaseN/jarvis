from openai import OpenAI
from dotenv import load_dotenv
import os
from modules.functions import sound
from tts import va_speak

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def sendQuest(text):
    try:
        sound('Сейчас_узнаю.mp3')
        text_str = ' '.join(text) if isinstance(text, list) else str(text)
        
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
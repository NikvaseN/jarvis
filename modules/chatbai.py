import os
import requests
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from tts import va_speak
from modules.functions import sound

load_dotenv()

TOKEN_GPT_AUTH = os.getenv("TOKEN_GPT_AUTH")
url = f"https://beta.theb.ai/api/conversation?org_id=427f29c6-7174-4adf-aa57-d94a5f95b3bf"

def remove_smileys(text):
    smiley_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002700-\U000027BF\U00002600-\U000026FF\U00002900-\U0000297F\U0001F900-\U0001F9FF\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F773]+'
    cleaned_text = re.sub(smiley_pattern, '', text)
    
    return cleaned_text


def sendQuest(text):
    sound('Сейчас_узнаю.mp3')
    text = ' '.join(text)
    data = {
        "text": text,
        "model": "7e682da4dde7ee214baa0efc0cf6d7a4",
        "model_params" : {"temperature": "1", "top_p": "1", "frequency_penalty": "0", "presence_penalty": "0", "long_term_memory": "ltm"}
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN_GPT_AUTH}'
    }

    response = ""

    r = requests.post(url=url, stream=True, json=data, headers=headers)

    for line in r.iter_lines(decode_unicode=True):
        if line.startswith('data:'):
            data = line.replace('data:', '')
            if (len(data) > 1):
                response = data

    json_data = json.loads(response)
    res = json_data['args']['content']
    res = remove_smileys(res)
    print(res)
    va_speak(res)
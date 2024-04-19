from modules.functions import sound
from translate import Translator
from tts import va_speak

def translate(text = None):
	if text is not None:
		sound('Перевожу.mp3')
		text = ' '.join(text)
		translator = Translator(from_lang='en', to_lang='ru')
		res = translator.translate(text)
		print(res)
		va_speak(res)

	else:
		sound('Неправильные_параметры.mp3')
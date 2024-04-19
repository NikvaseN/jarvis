import pyttsx3

engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')

engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

def va_speak(text):
	engine.say(text)
	engine.runAndWait()

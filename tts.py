import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

def va_speak(text):
    if not engine._inLoop:
        engine.say(text)
        engine.runAndWait()
    else:
        engine.endLoop()
        engine.say(text)
        engine.runAndWait()
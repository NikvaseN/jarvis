import speech_recognition as sr
from commands import commands
import winsound

# создаем экземпляр класса Recognizer
recognizer = sr.Recognizer()

while True:
    # записываем звук с микрофона
    with sr.Microphone() as source:
        print("Слушаю: ")
        audio_data = recognizer.listen(source, phrase_time_limit=5)

    # распознаем речь с помощью Google Speech Recognition
    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        print("Вы сказали: " + text)
        if "николас" in text.lower():
            index = text.lower().index("николас")
            winsound.Beep(350, 200)
            # Текст команды после обращения
            command_after_wake_word = text[index + len("николас"):].strip()
            # print("Команда после фразы 'ник': " + command_after_wake_word)
            # Массив слов из команды
            c = command_after_wake_word.split()
            # print(c)
            
            # Формируем ключ для поиска в словаре команд
            key = ' '.join(c[:2]) if len(c) >= 2 else ' '.join(c)
            key = key.lower()
            
            if key in commands:
                if len(c) > 2:
                    commands[key](c[2:])
                else:
                    commands[key]()
            
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass

import speech_recognition as sr
from commands import commands, get_closest_command
from dotenv import load_dotenv
import sys
from tts import va_speak
from modules.functions import find_command, sound
import traceback
import threading
from core.config import settings

# создаем экземпляр класса Recognizer
recognizer = sr.Recognizer()

load_dotenv()

triggerWords = settings.triggerWords

def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)
sys.excepthook = show_exception_and_exit

lastCommand = {}

def execute_command(command_func, *args):
    command_thread = threading.Thread(target=command_func, args=args)
    command_thread.start()

while True:
    with sr.Microphone() as source:
        # print("Слушаю: ")
        audio_data = recognizer.listen(source, phrase_time_limit=5)
    try:
        data = recognizer.recognize_google(audio_data, language="ru-RU")
        print("Вы сказали: " + data)

        data = data.lower()
        if any(keyword in data for keyword in triggerWords):
            # Ищем какое триггерное слово было сказано
            found_index = None
            for keyword in triggerWords:
                if keyword in data:
                    found_index = data.index(keyword)
                    break
            if found_index is not None:
                command = data[found_index + len(keyword):].strip()
                print(command)

                if (command in ["повтори команду", "ещё раз"]):
                    if len(lastCommand['text']) > 0:
                        execute_command(commands[lastCommand['c']], lastCommand['text'])
                    else:
                        execute_command(commands[lastCommand['c']])
                    continue

                c, text = find_command(command, commands)
                # print(c, text)
                
                if c is None:
                    sound('Неверная_команда.mp3')
                    print("Такой команды нет: " + command)
                    continue
                
                lastCommand = {'c': c, 'text': text}

                if len(text) > 0:
                    execute_command(commands[c], text)
                else:
                    execute_command(commands[c])
            
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass
    except:
        continue
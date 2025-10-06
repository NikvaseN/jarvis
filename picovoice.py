import speech_recognition as sr
from commands import commands, get_closest_command
import winsound
import pvporcupine
import struct
import pyaudio
from dotenv import load_dotenv
import sys, os
from tts import va_speak
from modules.functions import imready, find_command, sound
from modules.changeVolume import set_volume_all
import traceback
import threading
from modules.checkUseFunc import checkUsageFunction

# создаем экземпляр класса Recognizer
recognizer = sr.Recognizer()

load_dotenv()

TOKEN_PORCUPINE = os.getenv("TOKEN_PORCUPINE")

def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)
sys.excepthook = show_exception_and_exit

def main():
    try:
        porcupine = None
        pa = None
        audio_stream = None
        print("Слушаю: ")
        imready()
        
        # Консольное управление в отдельном потоке
        console_thread = threading.Thread(target=console_input_handler, daemon=True)
        console_thread.start()
        
        porcupine = pvporcupine.create(access_key=TOKEN_PORCUPINE, keywords=['alexa'])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from('h' * (len(pcm) // 2), pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0 :
                # Была сказана фраза
                listening()
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()

lastCommand = {}

def execute_command(command_func, *args):
    def wrapper():
        voice_req = checkUsageFunction(command_func, 'va_speak')
        if voice_req: # Если результат функции должен быть озвучен, то прибавлять звук после озвучки
            command_func(*args)
            set_volume_all(1)
        else:
            set_volume_all(1)
            command_func(*args)
    command_thread = threading.Thread(target=wrapper)
    command_thread.start()

def listening ():
    global lastCommand
    with sr.Microphone() as source:
        set_volume_all()
        winsound.Beep(350, 200)
        # sound('Слушаю.mp3')
        audio_data = recognizer.listen(source, phrase_time_limit=5)
    try:
        data = recognizer.recognize_google(audio_data, language="ru-RU")
        
        if (data in ["повтори команду", "ещё раз", 'выполни прошлую команду']):
            if len(lastCommand['text']) > 0:
                execute_command(commands[lastCommand['c']], lastCommand['text'])
            else:
                execute_command(commands[lastCommand['c']])
            return

        c, text = find_command(data, commands)
        # print(c, text)
        
        if c is None:
            sound('Неверная_команда.mp3')
            print("Такой команды нет: " + data)
            set_volume_all(1)
            return
        
        lastCommand = {'c': c, 'text': text}

        if len(text) > 0:
            execute_command(commands[c], text)
        else:
            execute_command(commands[c])
            
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass

def console_input_handler():
    # Обработчик консольного ввода
    
    global lastCommand
    
    while True:
        try:
            user_input = input("\nВведите команду: ").strip()
            
            if user_input.lower() in ['повтори команду', 'ещё раз']:
                if lastCommand:
                    if len(lastCommand['text']) > 0:
                        execute_command(commands[lastCommand['c']], lastCommand['text'])
                    else:
                        execute_command(commands[lastCommand['c']])
                else:
                    print("Нет предыдущей команды для повторения")
                continue
            
            c, text = find_command(user_input, commands)
            
            if c is None:
                print(f"Такой команды нет: {user_input}")
                continue
            
            lastCommand = {'c': c, 'text': text}
            
            if len(text) > 0:
                execute_command(commands[c], text)
            else:
                execute_command(commands[c])
                
        except KeyboardInterrupt:
            print("\nЗавершение работы...")
            os._exit(0)
        except Exception as e:
            print(f"Ошибка при обработке команды: {e}")

if __name__ == "__main__":
    main()
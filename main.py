import speech_recognition as sr
from commands import commands, get_closest_command
import winsound
import pyaudio
import sys, os
from tts import va_speak
from modules.functions import imready, find_command, sound
from modules.changeVolume import set_volume_all
import traceback
import threading
from pymicro_wakeword import MicroWakeWord, MicroWakeWordFeatures, Model
import numpy as np

recognizer = sr.Recognizer()

WAKE_WORD_MODEL = Model.ALEXA
SAMPLE_RATE = 16000
CHUNK_SIZE = 160


def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)
sys.excepthook = show_exception_and_exit


def main():
    try:
        pa = None
        audio_stream = None
        print("Слушаю: ")
        imready()
        
        console_thread = threading.Thread(target=console_input_handler, daemon=True)
        console_thread.start()
        
        print("[WakeWord] Инициализация microWakeWord...")
        mww = MicroWakeWord.from_builtin(WAKE_WORD_MODEL)
        mww_features = MicroWakeWordFeatures()
        
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=SAMPLE_RATE,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=CHUNK_SIZE
        )

        while True:
            raw_bytes = audio_stream.read(CHUNK_SIZE, exception_on_overflow=False)
            
            for features in mww_features.process_streaming(raw_bytes):
                if mww.process_streaming(features):
                    print(f"[WakeWord] Обнаружено: Алекса!")
                    listening()
                    mww_features.reset()
                    mww.reset()
                    break
                    
    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()

lastCommand = {}

def execute_command(command_func, *args):
    def wrapper():
        try:
            command_func(*args)
        finally:
            set_volume_all(1)
    command_thread = threading.Thread(target=wrapper)
    command_thread.start()

def listening():
    global lastCommand
    with sr.Microphone() as source:
        set_volume_all()
        winsound.Beep(350, 200)
        try:
            audio_data = recognizer.listen(source, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            winsound.Beep(200, 200)
            set_volume_all(1)
            return 
    try:
        data = recognizer.recognize_google(audio_data, language="ru-RU")
    
        
        if (data in ["повтори команду", "ещё раз", 'выполни прошлую команду']):
            if len(lastCommand['text']) > 0:
                execute_command(commands[lastCommand['c']], lastCommand['text'])
            else:
                execute_command(commands[lastCommand['c']])
            return

        c, text = find_command(data, commands)
        
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
        set_volume_all(1)
    except sr.RequestError as e:
        set_volume_all(1)

def console_input_handler():
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
import speech_recognition as sr
from commands import commands, get_closest_command
import winsound
import pvporcupine
import struct
import pyaudio
from dotenv import load_dotenv
import sys, os
from tts import va_speak
from modules.functions import imready, find_command
import traceback

# создаем экземпляр класса Recognizer
recognizer = sr.Recognizer()

load_dotenv()

TOKEN = os.getenv("TOKEN")

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
        porcupine = pvporcupine.create(access_key=TOKEN, keywords=['alexa'])
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

def listening ():
    # while True:
        with sr.Microphone() as source:
            winsound.Beep(350, 200)
            audio_data = recognizer.listen(source, phrase_time_limit=3)
        try:
            data = recognizer.recognize_google(audio_data, language="ru-RU")
            
            c, text = find_command(data, commands)

            # print(c)
            # print(text)

            if c is None:
                print("Такой команды нет: " + data)
                return
            
            if len(text) > 0:
                commands[c](text)
            else:
                commands[c]()
                
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            pass

main()
import speech_recognition as sr
from commands import commands, get_closest_command
import winsound
import pvporcupine
import struct
import pyaudio
from TOKENpicovoice import TOKEN
import sys

# создаем экземпляр класса Recognizer
recognizer = sr.Recognizer()

def show_exception_and_exit(exc_type, exc_value, tb):
	import traceback
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
        
        porcupine = pvporcupine.create(access_key=TOKEN, keywords=['jarvis'])
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
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            
            c = text.split()
            # Формируем ключ для поиска в словаре команд
            key = ' '.join(c[:2]) if len(c) >= 2 else ' '.join(c)
            key = key.lower()

            closest_command = get_closest_command(key, commands)

            if closest_command in commands:
                if len(c) > 2:
                    commands[closest_command](c[2:])
                else:
                    commands[closest_command]() 
            else:
                print("Такой команды нет: " + text)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            pass

main()
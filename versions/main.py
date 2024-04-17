import vosk
from commands import commands, get_closest_command
import winsound, json, pyaudio
import sys

model = vosk.Model('small-vosk-model')
rec = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

triggerWord = ['ник', 'миг', 'мик', 'ника', 'лик', 'пик', 'них', 'ним', 'николас', 'книг']
# triggerWord = ['джарвис', 'джарвс', 'гаррис', 'чарли', 'чарльз', 'гарри', 'джо', 'джайлс', 'джакс']

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    winsound.Beep(1000, 600)
    input("Press key to exit.")
    sys.exit(-1)
sys.excepthook = show_exception_and_exit

while True:
    try:
        data = stream.read(4000, exception_on_overflow=False)
        if(rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            text = answer['text']
            if text:
                print(text)
                if any(keyword in text.lower() for keyword in triggerWord):
                    # Ищем какое триггерное слово было сказано
                    found_index = None
                    for keyword in triggerWord:
                        if keyword in text.lower():
                            found_index = text.lower().index(keyword)
                            break
                    if found_index is not None:
                        command_after_wake_word = text[found_index + len(keyword):].strip()
                        c = command_after_wake_word.split()
                        
                        key = ' '.join(c[:2]) if len(c) >= 2 else ' '.join(c)
                        key = key.lower()

                        closest_command = get_closest_command(key, commands)
                        if closest_command in commands:
                            if len(c) > 2:
                                commands[closest_command](c[2:])
                            else:
                                commands[closest_command]()
                        else:
                            winsound.Beep(350, 200)
    except:
        pass
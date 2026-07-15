import threading
import queue
import pyttsx3
from modules.changeVolume import set_volume_all

VOLUME_REDUCTION = 0.05

_queue = queue.Queue()
_engine = None


def _tts_worker():
    global _engine
    _engine = pyttsx3.init()
    _engine.setProperty('rate', 200)
    _engine.setProperty('volume', 0.9)
    while True:
        text = _queue.get()
        try:
            set_volume_all(VOLUME_REDUCTION)
            _engine.say(text)
            _engine.runAndWait()
        except Exception as e:
            print(f"[TTS] Ошибка: {e}")
        finally:
            set_volume_all(1)
            _queue.task_done()


_worker_thread = threading.Thread(target=_tts_worker, daemon=True)
_worker_thread.start()


def va_speak(text: str, wait: bool = True):
    if not text:
        return
    _queue.put(text)
    if wait:
        _queue.join()
import sys, os
import psutil
from config import games, URL_SOUNDS
import winsound
import subprocess
from fuzzywuzzy import process
import ctypes
from modules.soundplay import soundplay
import threading
def sound(url = None):
    if url is None:
        winsound.Beep(300, 200)
        winsound.Beep(500, 200)
    else:
        soundplay(os.path.join(URL_SOUNDS, url))

def closing():
    sound('Закрываю.mp3')

def opening():
    sound('Открываю.mp3')

def starting():
    sound('Запускаю.mp3')

def imready():
    sound('Готов_к_работе.mp3')
        
def error():
    soundplay(os.path.join(URL_SOUNDS, 'Что_то_пошло_не_так.mp3'))

def killProcess(names):
    if isinstance(names, list):
        for proc in psutil.process_iter():
            try:
                for name in names:
                    if name.lower() in proc.name().lower():
                        proc.kill()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
    elif isinstance(names, str):
        for proc in psutil.process_iter():
            try:
                if name.lower() in proc.name().lower():
                    proc.kill()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

def startProcess(url) :
    starting()
    subprocess.Popen(url)
    
def startAdminProcess(url) :
    starting()
    ctypes.windll.shell32.ShellExecuteW(None, "runas", url, None, None, 1)
    
def closeGames():
    closing()
    killProcess(games)

def get_closest_match(text, KEYWORDS):
    closest_match, _ = process.extractOne(text, KEYWORDS.keys())
    return closest_match

def getUrl(user_input, KEYWORDS, URLS):
    if user_input is not None:
        user_input = ' '.join(user_input)
        name = user_input.lower()
        if name in URLS:
            return URLS[name]
        elif name in KEYWORDS:
            return URLS[KEYWORDS[name]]
        else:
            None
    else:
        None
        
def restartMe ():
    subprocess.Popen(['python', r'C:\Users\User0\Desktop\Jarvis\main2.py'])
    os._exit(0)

def find_command(text, commands):
    text_split = text.lower().split()
    for i in range(len(text_split), 0, -1):  # Проверяем от самого длинного к самому короткому
        key = ' '.join(text_split[:i])
        if key in commands:
            return key, text_split[i:]
    return None, None
	
def print_active_threads():
    for thread in threading.enumerate():
        print(f"Активный поток: {thread.name}")
    
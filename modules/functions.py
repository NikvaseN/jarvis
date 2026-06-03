import sys, os
import time
import psutil
from config import games_Processes, URL_SOUNDS, buttons, MAIN_SCRIPT
import winsound
import subprocess
from fuzzywuzzy import process
import ctypes
from modules.soundplay import soundplay
import threading
from tts import va_speak
import pyautogui
from datetime import datetime
import pyperclip
import re

def sound(url=None, wait=False):
    def play_sound():
        soundplay(os.path.join(URL_SOUNDS, url))
    if wait:
        # Запускаем в основном потоке — ждём
        play_sound()
    else:
        # Запускаем в отдельном потоке — не ждём
        sound_thread = threading.Thread(target=play_sound)
        sound_thread.start()
	

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
    elif isinstance(names, dict):
        for proc in psutil.process_iter():
            try:
                proc_name_lower = proc.name().lower()
                for value in names.values():
                    if value.lower() in proc_name_lower:
                        proc.kill()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
    else:
        sound('Неправильные_параметры.mp3')

# def startProcess(url) :
#     starting()
#     subprocess.Popen([url, ])

def startProcess(url):
    try:
        subprocess.Popen([url])
    except Exception as e:
        print(f"Ошибка: {e}")
        error()
    else:
        starting()
    
def startAdminProcess(url) :
    starting()
    ctypes.windll.shell32.ShellExecuteW(None, "runas", url, None, None, 1)
    
def closeGames():
    closing()
    killProcess(games_Processes)

def get_closest_match(text, KEYWORDS):
    closest_match, _ = process.extractOne(text, KEYWORDS.keys())
    return closest_match

def getUrl(user_input, URLS):
    if user_input is not None:
        user_input = ' '.join(user_input)
        name = user_input.lower()
        # print(name)
        # print(URLS)
        if name in URLS:
            return URLS[name]
        else:
            for key in URLS:
                value = URLS[key]
                if isinstance(key, tuple):
                    for alias in key:
                        # print(alias, name)
                        if alias == name:
                            # print(value)
                            return value
                elif key == name:
                    return value
        return None
    else:
        return None
        
def restartMe ():
    sound('Хорошо.mp3')
    time.sleep(1)
    subprocess.Popen(['python', MAIN_SCRIPT])
    os._exit(0)

def find_command(text, commands):
    text_split = text.lower().split()
    for i in range(len(text_split), 0, -1):
        key = ' '.join(text_split[:i])
        for command_key in commands:
            if isinstance(command_key, tuple):
                for alias in command_key:
                    if alias == key:
                        return command_key, text_split[i:]
            else:
                if command_key == key:
                    return command_key, text_split[i:]
    return None, None
    
def print_active_threads():
    for thread in threading.enumerate():
        print(f"Активный поток: {thread.name}")
    

def openClips ():
    opening()
    os.system(r'start E:\Видио')

def closeSelf ():
    opening()
    os._exit(0)
    
def press_button(button = None):
    try:
        if button is not None:
            buttonFind = getUrl(button, buttons)
            sound('Нажимаю.mp3')
            if(buttonFind):
                pyautogui.press(buttonFind)
            else: 
                pyautogui.press(button)
        else:
            sound('Неправильные_параметры.mp3')
    except:
        sound('Что_то_пошло_не_так.mp3')
        
def now_time():
    current_time = datetime.now().strftime("%H:%M")
    va_speak(current_time)
        
def copy(data):
    pyperclip.copy(data)

def remove_smileys(text):
    smiley_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002700-\U000027BF\U00002600-\U000026FF\U00002900-\U0000297F\U0001F900-\U0001F9FF\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F773]+'
    cleaned_text = re.sub(smiley_pattern, '', text)
    
    return cleaned_text
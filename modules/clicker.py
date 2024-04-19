import pyautogui
import time
import threading
from modules.functions import sound

clicker_running = False

def clicker_thread():
    global clicker_running
    while clicker_running:
        pyautogui.click()
        time.sleep(0.01)

def start_clicker():
    global clicker_running
    if not clicker_running:
        sound('Включаю.mp3')
        clicker_running = True
        threading.Thread(target=clicker_thread).start()

def stop_clicker():
    global clicker_running
    if clicker_running:
        sound('Выключаю.mp3')
        clicker_running = False
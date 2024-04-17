import os
import psutil
from config import games
import winsound
import subprocess
from fuzzywuzzy import process

def successfully():
    winsound.Beep(300, 200)
    winsound.Beep(500, 200)
    
def error():
    winsound.Beep(200, 200)

def killProcess(names):
    if isinstance(names, list):
        for proc in psutil.process_iter():
            try:
                for name in names:
                    if name.lower() in proc.name().lower():
                        proc.kill()
                        successfully()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
    elif isinstance(names, str):
        for proc in psutil.process_iter():
            try:
                if name.lower() in proc.name().lower():
                    proc.kill()
                    successfully()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

def startProcess(url) :
    subprocess.Popen([url])
    successfully()
    
def closeGames():
    killProcess(games)

def get_closest_match(text, KEYWORDS):
    closest_match, _ = process.extractOne(text, KEYWORDS.keys())
    return closest_match

def getUrl(user_input, KEYWORDS, URLS):
    if user_input is not None:
        user_input = ' '.join(user_input)
        name = user_input.lower()
        closest_match = get_closest_match(name, KEYWORDS)
        if name in URLS:
            return URLS[name]
        elif closest_match in KEYWORDS:
            return URLS[KEYWORDS[closest_match]]
        else:
            None
    else:
        error()
    
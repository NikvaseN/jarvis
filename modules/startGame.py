import subprocess
import os
from modules.functions import startProcess, getUrl, error, startAdminProcess
from core.config import settings
from tts import va_speak

URLS = settings.games_URLS
adminGames = settings.adminGames

def getGameFromURL(url, urls):
    for game, game_url in urls.items():
        if url == game_url:
            return game
    return None

def startGame(name = None):
    try:
        if name is not None:
            url = getUrl(name, URLS)
            game = getGameFromURL(url, URLS)
            if game in adminGames:
                startAdminProcess(url)
            else:
                startProcess(url)
        else:
            va_speak('Название игры в спике игр не найдена или что-то пошло не так! Проверьте список игр в конфиге')
    except:
        error()
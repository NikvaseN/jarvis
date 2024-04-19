import subprocess
import os
from modules.functions import startProcess, getUrl, error, startAdminProcess
from config import games_URLS as URLS, games_KEYWORDS as KEYWORDS, adminGames

def getGameFromURL(url, urls):
    for game, game_url in urls.items():
        if url == game_url:
            return game
    return None

def startGame(name = None):
    try:
        if name is not None:
            url = getUrl(name, KEYWORDS, URLS)
            game = getGameFromURL(url, URLS)
            if game in adminGames:
                startAdminProcess(url)
            else:
                startProcess(url)
        else:
            error()
    except:
        error()
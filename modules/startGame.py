import subprocess
import os
from modules.functions import startProcess, getUrl, error
from config import games_URLS as URLS, games_KEYWORDS as KEYWORDS

def startGame(name = None):
	if name is not None:
		url = getUrl(name, KEYWORDS, URLS)
		startProcess(url)
	else:
		error()
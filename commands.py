from modules.openSite import openSite
from modules.startDegree import startDegree
from modules.startGame import startGame
from modules.functions import closeGames, successfully
import os, sys
from fuzzywuzzy import process
import winsound

def get_closest_command(text, commands):
    closest_match, _ = process.extractOne(text, commands.keys())
    return closest_match

def empty (emp = None):
	winsound.Beep(350, 200)
    
commands = {
    "открой": empty,
    "закрой": empty,
    "запусти": empty,
    
    "открой сайт": openSite,
    "открой демки": lambda: os.system(r'start E:\Видио'),
    "открой клипы": lambda: os.system(r'start E:\Видио'),
    
    "запусти диплом": startDegree,
    "запусти игру": startGame,
    
    "закрой игру": closeGames,
    "закрой себя": lambda: os._exit(0),
}
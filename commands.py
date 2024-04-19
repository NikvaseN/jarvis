from modules.openSite import openSite
from modules.startDegree import startDegree
from modules.startGame import startGame
from modules.functions import closeGames, restartMe, print_active_threads
from modules.translate import translate
from modules.weather import weather
from modules.clicker import start_clicker, stop_clicker

import os, sys
from fuzzywuzzy import process
import winsound
from tts import va_speak

def get_closest_command(text, commands):
    closest_match, _ = process.extractOne(text, commands.keys())
    return closest_match

def empty (emp = None):
	winsound.Beep(350, 200)

def show_all_commads ():
	print("Команды:")
	for key in commands.keys():
		print(key)

commands = {
    "открой": empty,
    "закрой": empty,
    "запусти": empty,
    
    "открой сайт": openSite,
    "открой клипы": lambda: os.system(r'start E:\Видио'),
    
    "запусти диплом": startDegree,
    "запусти игру": startGame,
    
    "перезапусти себя": restartMe,

    "переведи": translate,
    "переведи слово": translate,
    
    "включи кликер": start_clicker,
    "включи clicker": start_clicker,
    
    "выключи кликер": stop_clicker,
    "выключи clicker": stop_clicker,
    
    "покажи потоки": print_active_threads,
    
    "покажи команды": show_all_commads,
    "покажи все команды": show_all_commads,
    
    "какая погода": weather,
    "какая сейчас погода": weather,
    
    "закрой игру": closeGames,
    "закрой себя": lambda: os._exit(0),
}
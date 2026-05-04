from modules.openSite import openSite
from modules.startDegree import startDegree
from modules.startGame import startGame
from modules.functions import *
from modules.translate import translate
from modules.weather import weather
from modules.clicker import start_clicker, stop_clicker
from modules.ai_chat import sendQuest
from modules.changeVolume import *

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
	print("------------------КОМАНДЫ--------------------", '\n')
	for key in commands.keys():
		print(key)

commands = {
    "открой": empty, "закрой": empty, "запусти": empty,

    ('stop', 'стоп'): restartMe,
    
    "открой сайт": openSite,
    ("открой клипы", 'открой демки'): openClips,
    
    "запусти диплом": startDegree,
    "запусти игру": startGame,
    
    "обновись": restartMe,

    ("переведи", "переведи слово"): translate,

    ("включи кликер", "включи clicker"): start_clicker,
    ("выключи кликер", "выключи clicker"): stop_clicker,
    
    "покажи потоки": print_active_threads,
    
	("покажи команды", "покажи все команды"): show_all_commads,

	("нажми", "нажми кнопку", 'нажми клавишу'): press_button,
    
    ("какая погода", "какая сейчас погода"): weather,

    ("узнай", "скажи"): sendQuest,

	("время", "сколько времени", "сколько время", 'сколько сейчас времени', 'сколько сейчас время'): now_time,

    ("выключи звук в", "выключи звук"): mute_application,
    ("включи звук в", "включи звук"): unmute_application,

    ("выключи весь звук"): mute_all,
    ("включи весь звук"): unmute_all,

    ("покажи все звуковые процессы", "покажи звуковые процессы"): print_sound_processes,

    
    "закрой игру": closeGames,
    "закрой себя": closeSelf,
}
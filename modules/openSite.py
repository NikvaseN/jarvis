import webbrowser
import winsound
from fuzzywuzzy import process
from config import sites_URLS as URLS
from modules.functions import opening, getUrl, error, sound

def openSite (que = None):
    try:
        url = getUrl(que, URLS)
        if url:
            opening()
            webbrowser.open(url, new=2)
        else:
            print(f'Ошибка: Неверное указание названия сайта или ключевого слова. Слово: {que}')
            sound('Увы_не_нашел.mp3')
    except:
        print('Что-то пошло не так при обработке названия сайта')
        error()
        

		

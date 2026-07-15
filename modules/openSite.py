import webbrowser
import winsound
from fuzzywuzzy import process
from core.config import settings
from modules.functions import opening, getUrl, error, sound

URLS = settings.sites_URLS

def openSite (que = None, say = True):
    try:
        if que.startswith(('http://', 'https://')):
            if say:
                opening()
            webbrowser.open(que)
            return
            
        url = getUrl(que, URLS)
        
        if url:
            if say:
                opening()
            webbrowser.open(url, new=2)
        else:
            print(f'Ошибка: Неверное указание названия сайта или ключевого слова. Слово: {que}')
            sound('Увы_не_нашел.mp3')
    except:
        print('Что-то пошло не так при обработке названия сайта')
        error()
        

		

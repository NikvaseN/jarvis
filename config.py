import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.absolute()

env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

def _get_required_env(key: str) -> str:
    """Получает переменную окружения или падает с понятной ошибкой."""
    value = os.getenv(key)
    if value is None:
        raise ValueError(
            f"Не найдена обязательная переменная окружения: {key}\n"
            f"Проверь файл .env в корне проекта: {env_path}"
        )
    return value

def _get_optional_env(key: str, default: str = "") -> str:
    """Получает переменную окружения или возвращает значение по умолчанию."""
    return os.getenv(key, default)

# -------------------ОСНОВНЫЕ НАСТРОЙКИ ПРОЕКТА-------------------------- #

# Пути
URL_SOUNDS = str(BASE_DIR / 'sounds' / 'lily') # Путь к папке с голосовыми ответами (файлы должны наываться идентично)
MAIN_SCRIPT = str(BASE_DIR / 'main.py')

CITY = _get_optional_env('CITY', '')

# ------------------------------API КЛЮЧИ-------------------------------- #

# AI Chat
API_KEY_GPT = _get_optional_env('API_KEY_GPT', '')

# Picovoice
PICOVOICE_KEY = _get_optional_env('PICOVOICE_KEY', '')

# Telegram бот
TELEGRAM_BOT_TOKEN = _get_optional_env('TELEGRAM_BOT_TOKEN', '')

# ------------------------------ВНЕШНИЕ URL------------------------------ #

WEATHER_URL = _get_optional_env('WEATHER_URL', '')

# ----------------------СПИСКИ (ИГРЫ, САЙТЫ, ПРИЛОЖЕНИЯ)------------------ #

# -----------------------------------САЙТЫ-------------------------------- #

sites_URLS = {
	('youtube', 'ютуба', 'ютуб'): 'https://www.youtube.com/',
	('translate', 'переводчика', 'переводчик'): 'https://translate.yandex.ru/translator/Русский-Английский',
	('vk', 'вк', 'вконтакте'): 'https://vk.com/',
	('genshin_interactive-map', 'интерактивной карты'): 'https://act.hoyolab.com/ys/app/interactive-map/index.html?lang=ru-ru#/map/2?shown_types=554&center=792.90,-3488.59&zoom=0.50',
	('синтеза речи'): 'https://elevenlabs.io/app/speech-synthesis',
}

# -----------------------------------ИГРЫ-------------------------------- #

games_URLS = {
	('cs 2', 'cs2', 'кс 2', 'кс2'): r'E:\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe',
	('ghostrunner', 'ghost runner'): r'E:\Games\Ghostrunner\Ghostrunner.exe',
	'genshin': r'E:\GenshinImpact\Genshin Impact game\GenshinImpact.exe',
	'city car driving': r'E:\Games\City Car Driving\SmartSteamLoader.exe',
}

adminGames = ['genshin'] # Игры которые нужно запускать от имени администратора

games_Processes = {
	('genshin', 'геншине', 'геншин'): "GenshinImpact.exe",
	('cs 2', 'cs2', 'кс 2', 'кс'): "cs2.exe",
	('dota', 'доте'): "dota2.exe",
	('brawlhalla'): "BrawlhallaGame.exe",
	('дрифт', 'дрифте', 'drift'): "TorqueDrift.exe",
	('content warning'): "Content Warning.exe",
}

ips = {
	('nipos', 'nibas', 'никаса'): 'connect 46.174.50.40:27015',
}

# -----------------------------------КЛАВИШИ-------------------------------- #

buttons = {
	('space', 'пробел', 'паузу', 'прыжок') : 'space', 
	('right', 'стрелку вправо') : 'right',
	('left', 'стрелку влево') : 'left',
	('f', 'full экран', 'полный экран') : 'f',
	('далее', 'вперед') : 'shift+n',
}

# -----------------------------------РАЗНОЕ-------------------------------- #

ignoreMute = ['python.exe', 
			  r'@%SystemRoot%\System32\AudioSrv.Dll,-202',
			  'sndvol.exe',
			  'audiodg.exe',
]

def validate_config():
    """Проверяет, что все необходимые настройки заданы."""
    warnings = []
    
    if not WEATHER_URL:
        warnings.append("WEATHER_URL не задан — команда погоды не будет работать")
    if not API_KEY_GPT:
        warnings.append("Не задан ни один API ключ для нейросетей - не получится задать вопрос ИИ")
    
    if warnings:
        print("⚠️  Предупреждения конфигурации:")
        for w in warnings:
            print(f"   - {w}")
        print()

# Автоматическая проверка при импорте
validate_config()
# -----------------------------------Проект-------------------------------- #

URL_SOUNDS = r'C:\Users\admin-vasiliy\Desktop\Jarvis\sounds\lily' # Изменить на свой путь к папке со звуками
triggerWords = ['алекса', 'алиса', 'алекс'] # Ключевая фраза
myUrl = r'C:\Users\admin-vasiliy\Desktop\Jarvis\picovoice.py' # Изменить на свой путь к файлу запуска бота


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

adminGames = ['genshin']

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
}

# -----------------------------------РАЗНОЕ-------------------------------- #

ignoreMute = ['python.exe', 
			  '@%SystemRoot%\System32\AudioSrv.Dll,-202',
			  'sndvol.exe',
			  'audiodg.exe',
]
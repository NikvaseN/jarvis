from pycaw.pycaw import AudioUtilities
from config import games_Processes, ignoreMute
from modules.functions import getUrl, sound

# Вывести все звуковые процессы
def print_sound_processes():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        print(session)

# Найти приложение по процессу и вернуть сессию
def find_application_by_name(name):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == name:
            return session

# Выключить весь звук
def mute_all(name = None):
    sessions = AudioUtilities.GetAllSessions()
    sound('Выключаю.mp3')
    for session in sessions:
        if session.Process: # Можно убрать, чтобы выключить звук всех процессов, в том числе системных
            if session.Process.name() in ignoreMute:
                continue
            session.SimpleAudioVolume.SetMute(1, None)

# Включить весь звук
def unmute_all(name = None):
    sound('Включаю.mp3')
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process: # Можно убрать, чтобы включить звук всех процессов, в том числе системных
            if session.Process.name() in ignoreMute:
                continue
            session.SimpleAudioVolume.SetMute(0, None)

# Выключить звук приложения
def mute_application(name):
    app_name = getUrl(name, games_Processes)
    application = find_application_by_name(app_name)
    if application is None:
        sound('Увы_не_нашел.mp3')
        return 
    sound('Выключаю.mp3')
    application.SimpleAudioVolume.SetMute(1, None)

# Включить звук приложения
def unmute_application(name):
    app_name = getUrl(name, games_Processes)
    application = find_application_by_name(app_name)
    if application is None:
        sound('Увы_не_нашел.mp3')
        return 
    sound('Включаю.mp3')
    application.SimpleAudioVolume.SetMute(0, None)


# volume_controller = app_session.SimpleAudioVolume
# new_volume = 0.5  # Например, устанавливаем громкость на половину
# volume_controller.SetMasterVolume(new_volume, None)
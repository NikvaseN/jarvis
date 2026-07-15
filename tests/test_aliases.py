import sys
from pathlib import Path

# Windows cp1251 fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))

from core.config import load_config

settings = load_config()

errors = []
total = 0
ok = 0


def check(label: str, got, expected):
    global total, ok
    total += 1
    if got == expected:
        ok += 1
    else:
        errors.append(f"  X {label}: polucheno {got!r}, ozhidalos {expected!r}")


SITE_URLS = {
    "youtube":                "https://www.youtube.com/",
    "translate":              "https://translate.yandex.ru/translator/Русский-Английский",
    "vk":                     "https://vk.com/",
    "youtube": "https://www.youtube.com/",
    "ютуба":   "https://www.youtube.com/",
    "ютуб":    "https://www.youtube.com/",
    "вк":      "https://vk.com/",
    "вконтакте": "https://vk.com/",
    "синтеза речи": "https://elevenlabs.io/app/speech-synthesis",
}

print("\nProverka saitov (sites.find)")
for alias, expected_url in SITE_URLS.items():
    got = settings.sites.find(alias)
    check(f"sites.find({alias!r})", got, expected_url)


GAME_PATHS = {
    "cs2": r"E:\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
    "кс 2": r"E:\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
    "genshin": r"E:\GenshinImpact\Genshin Impact game\GenshinImpact.exe",
}

print("\nProverka igr -- puti (games.find_url)")
for alias, expected_path in GAME_PATHS.items():
    got = settings.games.find_url(alias)
    check(f"games.find_url({alias!r})", got, expected_path)


GAME_PROCESSES = {
    "genshin": "GenshinImpact.exe",
    "геншин":  "GenshinImpact.exe",
    "геншине": "GenshinImpact.exe",
    "cs2":     "cs2.exe",
    "кс":      "cs2.exe",
    "кс 2":    "cs2.exe",
    "доте":    "dota2.exe",
}

print("\nProverka igr -- processi (games.find_process)")
for alias, expected_proc in GAME_PROCESSES.items():
    got = settings.games.find_process(alias)
    check(f"games.find_process({alias!r})", got, expected_proc)


BUTTON_KEYS = {
    "space":  "space",
    "пробел": "space",
    "right":  "right",
    "left":   "left",
    "next":   "shift+n",
    "далее":  "shift+n",
}

print("\nProverka knavish (buttons_cfg.find)")
for alias, expected_key in BUTTON_KEYS.items():
    got = settings.buttons_cfg.find(alias)
    check(f"buttons_cfg.find({alias!r})", got, expected_key)


IP_HOSTS = {
    "nipos":  "connect 46.174.50.40:27015",
    "nibas":  "connect 46.174.50.40:27015",
    "никаса": "connect 46.174.50.40:27015",
}

print("\nProverka IP (ips_cfg.find)")
for alias, expected_ip in IP_HOSTS.items():
    got = settings.ips_cfg.find(alias)
    check(f"ips_cfg.find({alias!r})", got, expected_ip)


print("\nProverka obratnoi sovmestimosti")
check("adminGames", settings.adminGames, ["genshin"])
check("CITY is str", isinstance(settings.CITY, str), True)
check("MAIN_SCRIPT endswith main.py", settings.MAIN_SCRIPT.endswith("main.py"), True)

print(f"\n{'='*50}")
print(f"Proideno: {ok} / {total}")
if errors:
    print(f"Oshibki ({len(errors)}):")
    for e in errors:
        print(e)
    sys.exit(1)
else:
    print(f"Vse proverki proideni uspeshno!")
    print(f"{'='*50}")

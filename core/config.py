"""
Конфигурация Jarvis — Pydantic v2 + YAML + .env.

Загружает:
  - config/settings.yaml   — основные настройки (списки, пути, алиасы)
  - .env                   — секреты (API-ключи, CITY)

Использование:
    from core.config import load_config
    settings = load_config()
    print(settings.secrets.api_key_gpt)

Обратная совместимость (старый config.py):
    games_URLS, sites_URLS, games_Processes, buttons, ips, etc.
    — всё доступно как свойства Settings.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
import yaml


# ──────────────────────────────────────────────
#  Вспомогательные функции
# ──────────────────────────────────────────────

def _project_root() -> Path:
    """Корень проекта (на два уровня выше core/config.py)."""
    return Path(__file__).parent.parent.resolve()


def _load_dotenv() -> None:
    """Загружаем .env из корня проекта."""
    env_path = _project_root() / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)


def _get_required_env(key: str) -> str:
    """Обязательная переменная окружения."""
    value = os.getenv(key)
    if value is None:
        raise ValueError(
            f"Не найдена обязательная переменная окружения: {key}\n"
            f"Проверь файл .env в корне проекта: {_project_root() / '.env'}"
        )
    return value


def _get_optional_env(key: str, default: str = "") -> str:
    """Опциональная переменная окружения."""
    return os.getenv(key, default)


# ──────────────────────────────────────────────
#  Вспомогательные утилиты для построения lookup
# ──────────────────────────────────────────────

def _build_flat_lookup(
    items: Dict[str, BaseModel],
    value_attr: str,
) -> Dict[str, str]:
    """Строит плоский dict {алиас → значение} для быстрого поиска.

    Для каждого элемента items сначала кладётся канонический ключ,
    затем все алиасы.  Регистронезависимо, с strip().
    """
    result: Dict[str, str] = {}
    for key, entry in items.items():
        value = getattr(entry, value_attr)
        result[key.lower()] = value
        for alias in getattr(entry, "aliases", []):
            result[alias.lower().strip()] = value
    return result


# ──────────────────────────────────────────────
#  Модели записей с алиасами
# ──────────────────────────────────────────────

class SiteEntry(BaseModel):
    """Одна запись сайта."""
    url: str
    aliases: List[str] = []


class GameUrlEntry(BaseModel):
    """Одна запись игры (путь к .exe)."""
    path: str
    aliases: List[str] = []


class ProcessEntry(BaseModel):
    """Одна запись процесса игры."""
    process: str
    aliases: List[str] = []


class ButtonEntry(BaseModel):
    """Одна запись сочетания клавиш."""
    key: str
    aliases: List[str] = []


class IpEntry(BaseModel):
    """Одна запись IP-адреса."""
    host: str
    aliases: List[str] = []


# ──────────────────────────────────────────────
#  Модели секций конфига
# ──────────────────────────────────────────────


class SitesConfig(BaseModel):
    """Список сайтов с алиасами."""

    urls: Dict[str, SiteEntry] = Field(default_factory=dict)

    def model_post_init(self, __context):
        self._lookup = _build_flat_lookup(self.urls, "url")

    def find(self, query: str) -> Optional[str]:
        """Найти URL по ключу или алиасу (регистронезависимо)."""
        return self._lookup.get(query.lower().strip())


class GamesConfig(BaseModel):
    """Игры — пути запуска, процессы, админ-права."""

    urls: Dict[str, GameUrlEntry] = Field(default_factory=dict)
    processes: Dict[str, ProcessEntry] = Field(default_factory=dict)
    admin: List[str] = Field(default_factory=list)

    def model_post_init(self, __context):
        self._urls_lookup = _build_flat_lookup(self.urls, "path")
        self._processes_lookup = _build_flat_lookup(self.processes, "process")

    def find_url(self, query: str) -> Optional[str]:
        """Найти путь к .exe по ключу или алиасу."""
        return self._urls_lookup.get(query.lower().strip())

    def find_process(self, query: str) -> Optional[str]:
        """Найти имя процесса по ключу или алиасу."""
        return self._processes_lookup.get(query.lower().strip())


class ButtonsConfig(BaseModel):
    """Сочетания клавиш с алиасами."""

    keys: Dict[str, ButtonEntry] = Field(default_factory=dict)

    def model_post_init(self, __context):
        self._lookup = _build_flat_lookup(self.keys, "key")

    def find(self, query: str) -> Optional[str]:
        """Найти клавишу по голосовой команде или алиасу."""
        return self._lookup.get(query.lower().strip())


class IpsConfig(BaseModel):
    """IP-адреса для подключения с алиасами."""

    hosts: Dict[str, IpEntry] = Field(default_factory=dict)

    def model_post_init(self, __context):
        self._lookup = _build_flat_lookup(self.hosts, "host")

    def find(self, query: str) -> Optional[str]:
        """Найти 'connect IP:port' по ключу или алиасу."""
        return self._lookup.get(query.lower().strip())


class AudioConfig(BaseModel):
    """Настройки аудио."""

    ignore_mute: List[str] = Field(
        default_factory=lambda: ["python.exe", "sndvol.exe", "audiodg.exe"],
        description="Процессы, которые не отключаем",
    )
    volume_reduction: float = Field(0.05, ge=0.0, le=1.0, description="Громкость при ответе")
    sample_rate: int = Field(16000, description="Частота дискретизации микрофона")
    trigger_words: List[str] = Field(
        default_factory=lambda: ["алекса", "jarvis", "джарвис"],
        description="Триггерные слова для NonWakeWord-режима",
    )


class PathsConfig(BaseModel):
    """Пути к ресурсам."""

    sounds_voice: str = Field("sounds/lily", description="Папка с голосовыми файлами")
    sounds_music: str = Field("sounds/josh", description="Папка с музыкой")


class WakeWordConfig(BaseModel):
    """Настройки wake-word."""

    model: str = Field("ALEXA", description="Встроенная модель MicroWakeWord")
    chunk_size: int = Field(160, description="Размер чанка аудио")


class LLMConfig(BaseModel):
    """Настройки LLM."""

    api_key: str = Field("", description="Ключ API")
    model: str = Field("llama-3.3-70b-versatile", description="Модель")
    temperature: float = Field(0.7, ge=0.0, le=2.0)


class STTConfig(BaseModel):
    """Настройки распознавания речи."""

    engine: str = Field("faster_whisper", description="Движок STT")
    model: str = Field("small", description="Модель faster-whisper")
    language: str = Field("ru", description="Язык")
    device: str = Field("cpu", description="Устройство (cpu/cuda)")
    compute_type: str = Field("int8", description="Тип вычислений (int8/float16/float32)")


class SecretsConfig(BaseModel):
    """Секреты из .env — API-ключи, токены, город."""

    api_key_gpt: str = Field("", description="Ключ для OpenAI / Groq")
    picovoice_key: str = Field("", description="Picovoice API-ключ")
    telegram_bot_token: str = Field("", description="Токен Telegram-бота")
    city: str = Field("", description="Город для погоды (из .env CITY)")

    @classmethod
    def from_env(cls) -> "SecretsConfig":
        _load_dotenv()
        return cls(
            api_key_gpt=_get_optional_env("API_KEY_GPT", ""),
            picovoice_key=_get_optional_env("PICOVOICE_KEY", ""),
            telegram_bot_token=_get_optional_env("TELEGRAM_BOT_TOKEN", ""),
            city=_get_optional_env("CITY", ""),
        )


# ──────────────────────────────────────────────
#  Корневая модель Settings
# ──────────────────────────────────────────────


class Settings(BaseModel):
    """Корневая модель конфигурации Jarvis."""

    paths: PathsConfig = Field(default_factory=PathsConfig)
    secrets: SecretsConfig = Field(default_factory=SecretsConfig)
    sites: SitesConfig = Field(default_factory=SitesConfig)
    games: GamesConfig = Field(default_factory=GamesConfig)
    buttons_cfg: ButtonsConfig = Field(default_factory=ButtonsConfig, alias="buttons")
    ips_cfg: IpsConfig = Field(default_factory=IpsConfig, alias="ips")
    audio: AudioConfig = Field(default_factory=AudioConfig)
    wake_word: WakeWordConfig = Field(default_factory=WakeWordConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    stt: STTConfig = Field(default_factory=STTConfig)

    model_config = {"populate_by_name": True}

    # ── обратная совместимость (старый config.py) ─────────────────

    @property
    def sites_URLS(self) -> Dict[str, str]:
        """Плоский dict: все алиасы → URL (как в старом config.py)."""
        return self.sites._lookup

    @property
    def games_URLS(self) -> Dict[str, str]:
        """Плоский dict: все алиасы → путь к .exe."""
        return self.games._urls_lookup

    @property
    def games_Processes(self) -> Dict[str, str]:
        """Плоский dict: все алиасы → имя процесса."""
        return self.games._processes_lookup

    @property
    def adminGames(self) -> List[str]:
        return self.games.admin

    @property
    def buttons(self) -> Dict[str, str]:
        """Плоский dict: все алиасы → клавиша."""
        return self.buttons_cfg._lookup

    @property
    def ips(self) -> Dict[str, str]:
        """Плоский dict: все алиасы → connect-строка."""
        return self.ips_cfg._lookup

    @property
    def ignoreMute(self) -> List[str]:
        return self.audio.ignore_mute

    @property
    def triggerWords(self) -> List[str]:
        return self.audio.trigger_words

    @property
    def URL_SOUNDS(self) -> str:
        return str(_project_root() / self.paths.sounds_voice)

    @property
    def MAIN_SCRIPT(self) -> str:
        return str(_project_root() / "main.py")

    @property
    def API_KEY_GPT(self) -> str:
        return self.secrets.api_key_gpt

    @property
    def PICOVOICE_KEY(self) -> str:
        return self.secrets.picovoice_key

    @property
    def TELEGRAM_BOT_TOKEN(self) -> str:
        return self.secrets.telegram_bot_token

    @property
    def CITY(self) -> str:
        """Город для погоды (из .env)."""
        return self.secrets.city

    @property
    def WEATHER_CITY(self) -> str:
        """Псевдоним для CITY (совместимость)."""
        return self.secrets.city


YAML_PATH = _project_root() / "config" / "settings.yaml"

# ── кеш (избегаем повторного чтения файлов при импорте в N модулях) ──
_settings_cache: Optional[Settings] = None


def load_config(
    yaml_path: Optional[Path] = None,
) -> Settings:
    """
    Загружает конфигурацию: YAML + .env → Pydantic-модель.

    Args:
        yaml_path: путь к settings.yaml (по умолчанию config/settings.yaml)

    Returns:
        Settings — провалидированная модель со всеми настройками.
    """
    if yaml_path is None:
        yaml_path = YAML_PATH

    # 1. Секреты из .env
    secrets = SecretsConfig.from_env()

    # 2. Основные настройки из YAML
    yaml_data: Dict[str, Any] = {}
    if yaml_path.exists():
        with open(yaml_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f) or {}

    # 3. Собираем модель (YAML сверху, .env снизу — secrets перетрёт YAML-значения)
    settings = Settings(**yaml_data)
    settings.secrets = secrets

    # 4. Валидация
    _validate(settings)

    global _settings_cache
    _settings_cache = settings
    return settings


def _validate(settings: Settings) -> None:
    """Выводит предупреждения о пропущенных настройках."""
    warnings: List[str] = []

    if not settings.secrets.api_key_gpt:
        warnings.append("API_KEY_GPT ne zadan -- voprosy II ne budut rabotat")
    if not settings.secrets.city:
        warnings.append("CITY ne zadan -- komanda pogody mozhet rabotat nekorrektno")

    if warnings:
        print("[!] Preduprezhdeniya konfiguracii:")
        for w in warnings:
            print(f"   - {w}")
        print()


# ──────────────────────────────────────────────
#  Единая точка входа: from core.config import settings
# ──────────────────────────────────────────────

class _LazySettings:
    """
    Прокси для ленивой загрузки Settings при первом обращении.

    Позволяет во всех модулях писать:
        from core.config import settings
        settings.games_Processes, settings.URL_SOUNDS, ...

    Без единого вызова load_config() в модулях.
    """

    def __init__(self) -> None:
        self._cached: Optional[Settings] = None

    def __getattr__(self, name: str):
        # Пропускаем служебные атрибуты (не отправляем их в Settings)
        if name.startswith("_"):
            raise AttributeError(name)
        if self._cached is None:
            self._cached = load_config()
        return getattr(self._cached, name)


settings: Any = _LazySettings()

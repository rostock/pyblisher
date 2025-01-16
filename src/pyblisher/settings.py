import sys
import tomllib
from pathlib import Path
from typing import Optional, Dict, Any


class Settings:
    _instance = None
    _settings: Dict[str, Any] = {
        'HOST': None,
        'API_KEY': None,
        'TIMEOUT': 30,
        # weitere Default-Werte hier
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._load_settings()
        return cls._instance

    def _load_settings(self) -> None:
        # 1. Versuche Django Settings zu laden
        if self._load_django_settings():
            return

        # 2. Versuche pyblisher.toml zu laden
        if self._load_toml_config():
            return

    def _load_django_settings(self) -> bool:
        try:
            from django.conf import settings
            if hasattr(settings, 'PYBLISHER'):
                self._settings.update(settings.PYBLISHER)
                return True
        except ImportError:
            return False
        return False

    def _load_toml_config(self) -> bool:
        try:
            # Suche pyblisher.toml im aktuellen Projektverzeichnis
            config_path = Path.cwd() / 'pyblisher.toml'
            if config_path.exists():
                with open(config_path, 'rb') as f:  # TOML muss im binary mode gelesen werden
                    config = tomllib.load(f)
                    if 'pyblisher' in config:  # Wir erwarten einen [pyblisher] Abschnitt
                        self._settings.update(config['pyblisher'])
                    return True
        except Exception as e:
            print(f"Warnung: Konnte pyblisher.toml nicht laden: {e}")
        return False

    def __getattr__(self, name: str) -> Any:
        if name in self._settings:
            return self._settings[name]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

settings = Settings()

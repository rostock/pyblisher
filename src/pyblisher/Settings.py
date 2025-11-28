import json
import tomllib
from datetime import datetime
from pathlib import Path

from dacite import Config

from .helpers import parse_datetime, parse_source_property
from .types import SourceProperty


class Settings:
    """Singleton class that loads settings from different sources.

    This class is a singleton that loads settings from different sources
    like Django settings, pyblisher.json, or pyproject.toml.

    Attributes:
        host: The host of the API.
        user: The user for the API.
        password: The password for the API.
        api_version: The version of the API.
        project_id: The project id.
    """

    _instance = None
    dacite_config = Config(
        type_hooks={
            datetime: parse_datetime,
            SourceProperty: parse_source_property,
        },
    )

    def __new__(cls):
        """Create a singleton instance of the Settings class.

        This is a singleton, so we only create one instance of this class.

        Returns:
            Settings: The singleton instance of the Settings class.
        """
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._load_settings()
        return cls._instance

    def _load_settings(self) -> None:
        """Try to load settings from different sources.

        This function tries to load settings from different sources in the
        following order:
        1. Django settings
        2. pyblisher.json
        3. pyproject.toml

        Raises:
            AttributeError: If no settings are found in any source.
        """
        # 1. Try to load settings from Django settings.
        if self._load_django_settings():
            print('loaded settings from Django settings')
            return

        # 2. Try to load settings from pyblisher.json.
        elif self._load_json_config():
            print('loaded settings from pyblisher.json')
            return

        # 3. Try to load settings from pyproject.toml.
        elif self._load_toml_config():
            print('loaded settings from pyproject.toml')
            return
        # If no settings are found, raise an AttributeError.
        else:
            print('no settings found')
            raise AttributeError(
                'Found no Settings in pyblisher.toml or Django settings.'
            )

    def _load_django_settings(self) -> bool:
        """Try to load settings from Django settings.

        Returns:
            bool: True if settings were loaded successfully, False otherwise.
        """
        try:
            from django.conf import settings  # type: ignore[import-not-found]

            if hasattr(settings, 'PYBLISHER'):
                for key, value in settings.PYBLISHER.items():
                    setattr(self, key.lower(), value)
                return True
        except ImportError:
            return False
        return False

    def _load_toml_config(self) -> bool:
        """Try to load settings from a pyproject.toml file.

        Looks for a pyproject.toml file in the current working directory
        and loads settings from the [pyblisher] section.

        Returns:
            bool: True if settings were loaded successfully, False otherwise.
        """
        try:
            # Look for pyproject.toml in the current project directory
            config_path = Path.cwd() / 'pyproject.toml'
            if config_path.exists():
                with open(
                    config_path, 'rb'
                ) as f:  # TOML must be read in binary mode
                    config = tomllib.load(f)
                    if 'pyblisher' in config:
                        # Look for [pyblisher] section in pyproject.toml
                        for key, value in config['pyblisher'].items():
                            setattr(self, key.lower(), value)
                    return True
        except Exception as e:
            print(f'Warning: Can not load pyblisher settings. {e}')
        return False

    def _load_json_config(self) -> bool:
        """Try to load settings from a pyblisher.json file.

        Looks for a pyblisher.json file in the current working directory
        and loads all settings from it.

        Returns:
            bool: True if settings were loaded successfully, False otherwise.
        """
        try:
            # Look for pyblisher.json in the current project directory
            config_path = Path.cwd() / 'pyblisher.json'
            if config_path.exists():
                with open(
                    config_path, 'r'
                ) as f:  # JSON must be read in text mode
                    config = json.load(f)
                    for key, value in config.items():
                        setattr(self, key.lower(), value)
                    return True
        except Exception as e:
            print(f'Warning: Can not load pyblisher settings. {e}')
        return False

    def __getattr__(self, name: str):
        """Handle attribute access for undefined attributes.

        Args:
            name: The name of the attribute being accessed.

        Raises:
            AttributeError: Always raised when an undefined attribute is accessed.
        """
        raise AttributeError(
            f"'{self.__class__.__name__}' has no attribute '{name}'"
        )

    def __repr__(self):
        """Return a string representation of the Settings instance.

        Returns:
            str: A string in the format ClassName(attr1=value1, attr2=value2, ...).
        """
        text = f'{self.__class__.__name__}('
        for key, value in self.__dict__.items():
            text += f'{key}={repr(value)}, '
        text = text[:-2] + ')'
        return text


settings = Settings()

import json
import tomllib
from datetime import datetime
from pathlib import Path

from dacite import Config

from .helpers import parse_datetime, parse_source_property
from .types import SourceProperty


class Settings:
    """
    This class is a singleton that loads settings from different sources.

    :attr host: The host of the API
    :atype host: str
    :attr user: The user for the API
    :atype user: str
    :attr password: The password for the API
    :atype password: str
    :attr api_version: The version of the API
    :atype api_version: str
    :attr project_id: The project id
    :atype project_id: str
    """

    _instance = None
    dacite_config = Config(
        type_hooks={
            datetime: parse_datetime,
            SourceProperty: parse_source_property,
        },
    )

    def __new__(cls):
        """
        This is a singleton, so we only create one instance of this class.
        """
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._load_settings()
        return cls._instance

    def _load_settings(self) -> None:
        """
        This function tries to load settings from different sources.
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
        """
        This function tries to load settings from Django settings.
        """
        try:
            from django.conf import settings

            if hasattr(settings, 'PYBLISHER'):
                for key, value in settings.PYBLISHER.items():
                    setattr(self, key.lower(), value)
                return True
        except ImportError:
            return False
        return False

    def _load_toml_config(self) -> bool:
        """
        This function tries to load settings from a pyblisher.toml file.
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
        """
        This function tries to load settings from a pyblisher.json file.
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
        """
        This function is called when an attribute is not found.
        """
        raise AttributeError(
            f"'{self.__class__.__name__}' has no attribute '{name}'"
        )

    def __repr__(self):
        """
        This function returns its state in the following format:
            ClassName(attr1=value1, attr2=value2, ...)
        every value is represented with its repr() function
        """
        text = f'{self.__class__.__name__}('
        for key, value in self.__dict__.items():
            text += f'{key}={repr(value)}, '
        text = text[:-2] + ')'
        return text


settings = Settings()

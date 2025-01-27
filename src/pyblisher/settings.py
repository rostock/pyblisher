import tomllib
from pathlib import Path


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
        # 1. Versuche Django Settings zu laden
        if self._load_django_settings():
            print('loaded settings from Django settings')
            return

        # 2. Versuche pyblisher.toml zu laden.
        elif self._load_toml_config():
            print('loaded settings from pyblisher.toml')
            return
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
            # Suche pyblisher.toml im aktuellen Projektverzeichnis
            config_path = Path.cwd() / 'pyblisher.toml'
            if config_path.exists():
                with open(
                    config_path, 'rb'
                ) as f:  # TOML muss im binary mode gelesen werden
                    config = tomllib.load(f)
                    if (
                        'pyblisher' in config
                    ):  # Wir erwarten einen [pyblisher] Abschnitt
                        # self._settings.update(config["pyblisher"])
                        for key, value in config['pyblisher'].items():
                            setattr(self, key.lower(), value)
                    return True
        except Exception as e:
            print(f'Warnung: Konnte pyblisher.toml nicht laden: {e}')
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

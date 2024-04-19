"""Linter configuration logic."""
from typing import Dict, Any

import pkg_resources
import yaml

_config = dict()
_read_default = False

_DEFAULT_CONFIG_FILE = 'bibla.yml'


def get_config() -> Dict:
    """Return the loaded config or instantiate and return default config."""
    if not _read_default:
        _load_default_config()
    return _config


def set_config(key: str, value: Any, default: bool = False):
    """Set a value in the configurations.

    :param key: configuration entry key
    :param value: configuration entry value
    :param default: If true, set as default value to be overwritten by later
    """
    if value is not None:
        if default:
            _config.setdefault(key, value)
        else:
            _config[key] = value
        _validate_and_clean_config(_config)


def load_config_file(file):
    """Read a YAML config file and use it as the configuration.

    :param file: .yaml config file path
    """
    with open(file) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        for k, v in config.items():
            set_config(k, v)


def _load_default_config():
    global _read_default
    _read_default = True
    with open(pkg_resources.resource_filename(__name__,
                                              _DEFAULT_CONFIG_FILE)) as \
            default_config_file:
        default_config = yaml.load(default_config_file, Loader=yaml.FullLoader)
        for k, v in default_config.items():
            set_config(k, v, default=True)


def _validate_and_clean_config(config):
    if 'select' in config and 'ignore' in config and config['select'] and \
            config['ignore']:
        raise ValueError(
            "Configuration cannot contain both included and selected and "
            "ignored rules. Use either include or exclude to select"
            "enabled rules."
        )

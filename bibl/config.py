import os

import yaml
import os

_DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../.bibl.yml')
_config = dict()


def load_config(file):
    global _config
    if not _config:
        _load_config(_DEFAULT_CONFIG_PATH)
    _load_config(file)


def get_config():
    global _config
    if not _config:
        _load_config(_DEFAULT_CONFIG_PATH)
    return _config


def set_config(key, value):
    global _config
    if not _config:
        _load_config(_DEFAULT_CONFIG_PATH)
    if not value is None:
        _config[key] = value
        if key in {'select', 'ignore'} and _config[key] is None:
            _config[key] = []
        _validate_config(_config)


def _load_config(file):
    global _config
    with open(file) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    for k, v in config.items():
        set_config(k, v)


def _validate_config(config):
    if 'select' in config and 'ignore' in config and config['select'] and config['ignore']:
        raise ValueError(
            "Configuration cannot contain both included and selected and ignored rules. Use either include or exclude to select"
            "enabled rules."
        )

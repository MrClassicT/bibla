import yaml
import os

_DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../.bibl.yml')
_config = {
    'select': [],
    'ignore': [],
    'indent_spaces': 0,
    'max_line_length': 0,
    'abbreviation_dot': False,
    'type_spec': dict(),
}

def load_config(config_file_path):
    global _config
    config = _load_config_file(config_file_path)
    for k, v in config.items():
        set_config(k, v)


def get_config():
    return _config


def set_config(key, value):
    global _config
    if not value is None and key in _config.keys():
        _config[key] = value
        if key in {'select', 'ignore'} and _config[key] is None:
            _config[key] = []
        _validate_config(_config)


def _load_config_file(path):
    with open(path) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config


def _validate_config(config):
    if config['select'] and config['ignore']:
        raise ValueError(
            "Configuration cannot contain both included and selected and ignored rules. Use either include or exclude to select"
            "enabled rules."
        )


load_config(_DEFAULT_CONFIG_PATH)

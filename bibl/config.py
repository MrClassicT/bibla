import pkg_resources
import yaml

_config = dict()

_DEFAULT_CONFIG_FILE = '.bib.yml'


def get_config():
    global _config
    if not _config:
        _load_default_config()
    return _config


def set_config(key, value):
    global _config
    if not _config:
        _load_default_config()
    if not value is None:
        _config[key] = value
        if key in {'select', 'ignore'} and _config[key] is None:
            _config[key] = []
        _validate_config(_config)


def load_config_file(file):
    with open(file) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        _load_config(config)


def _load_config(config):
    for k, v in config.items():
        set_config(k, v)


def _load_default_config():
    with open(pkg_resources.resource_filename(_DEFAULT_CONFIG_FILE, "resourcefile")) as default_config_file:
        default_config = yaml.load(default_config_file, Loader=yaml.FullLoader)
        _load_config(default_config)


def _validate_config(config):
    if 'select' in config and 'ignore' in config and config['select'] and config['ignore']:
        raise ValueError(
            "Configuration cannot contain both included and selected and ignored rules. Use either include or exclude to select"
            "enabled rules."
        )

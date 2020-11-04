import fnmatch
import os
from typing import Callable, Dict, List
from importlib import import_module
from pybtex.database import Entry

from bibl.config import get_config


class Rule():

    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description
        self._rule = None

    def __str__(self):
        return "{}: {}".format(self.id, self.description)

    def __call__(self, *args, **kwargs):
        return self._rule(*args, **kwargs)

    @property
    def enabled(self):
        if get_config()['select']:
            for pattern in get_config()['select']:
                if fnmatch.fnmatch(self.id, pattern):
                    return True
            return False
        if get_config()['ignore']:
            for pattern in get_config()['ignore']:
                if fnmatch.fnmatch(self.id, pattern):
                    return False
            return True
        return True


class EntryRule(Rule):

    def __init__(self, id, description, rule: Callable[[str, Entry, Dict[str, Entry]], bool], **kwargs):
        super().__init__(id, description)
        self._rule = rule


class TextRule(Rule):

    def __init__(self, id, description, rule: Callable[[int, str, str], bool], **kwargs):
        super().__init__(id, description)
        self._rule = rule


class RuleStore:

    def __init__(self):
        self._rules = []

    def register(self, rule: Rule):
        position = 0
        while position < len(self._rules) and self._rules[position].id < rule.id:
            position += 1
        self._rules.insert(position, rule)

    @property
    def all(self) -> List[Rule]:
        return self._rules

    @property
    def enabled(self) -> List[Rule]:
        return [rule for rule in self._rules if rule.enabled]

    @property
    def enabled_entry_rules(self) -> List[EntryRule]:
        return [rule for rule in self.enabled if isinstance(rule, EntryRule)]

    @property
    def enabled_text_rules(self) -> List[TextRule]:
        return [rule for rule in self.enabled if isinstance(rule, TextRule)]


_ALL_RULES: RuleStore = RuleStore()


def register_entry_rule(id, description: str):
    def decorator(f: Callable[[str, Entry, Dict[str, Entry]], bool]):
        rule = EntryRule(id, description, f)
        _ALL_RULES.register(rule)

    return decorator


def register_text_rule(id: str, description: str):
    def decorator(f: Callable[[int, str, str], bool]):
        rule = TextRule(id, description, f)
        _ALL_RULES.register(rule)

    return decorator


def load_rules() -> RuleStore:
    for module in os.listdir(os.path.join(os.path.dirname(__file__), 'rules')):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        __import__('bibl.rules.' + module[:-3], locals(), globals())
    del module
    return _ALL_RULES

from typing import Callable, Dict

from pybtex.database import Entry


class Rule():

    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description
        self._rule = None

    def __call__(self, *args, **kwargs):
        return self._rule(*args, **kwargs)


class RuleStore:

    def __init__(self):
        self._rules = dict()
        self._enabled = dict()

    def register(self, rule: Rule):
        self._rules[rule.id] = rule
        self._enabled[rule.id] = True

    @property
    def enabled(self):
        enabled = dict()
        for id, rule in self._rules.items():
            if self._enabled[id]:
                enabled[id] = rule
        return enabled


class EntryRule(Rule):

    def __init__(self, id, description, rule: Callable[[str, Entry, Dict[str, Entry]], bool], **kwargs):
        super().__init__(id, description)
        self._rule = rule


_ENTRY_RULES = RuleStore()


def register_entry_rule(id, description):
    def decorator(f):
        rule = EntryRule(id, description, f)
        _ENTRY_RULES.register(rule)
    return decorator


def load_entry_rules() -> RuleStore:
    from bibl.rules import entry_rules, field_rules
    return _ENTRY_RULES

"""Structure to manage rules in a unified way."""
import fnmatch
import os
from typing import Callable, Dict, List
from pybtex.database import Entry
from bibla.config import get_config


class Rule:
    """Generic rule class.

    :param rule_id: identifying code for this rule, starting with a letter
    indicating the rule type, followed by a number or a string specification.
    :param description: a full sentence description of the rule
    """

    def __init__(self, rule_id: str, description: str, rule: Callable):
        """Create Rule object.

        :param rule_id: identifying code for this rule, starting with a letter
        indicating the rule type, followed by a number or a string
        specification.
        :param description: a full sentence description of the rule
        :param rule: a callable returning a boolean to execute when checking
        this rule
        """
        self.rule_id = rule_id
        self.description = description
        self._rule = rule

    def __str__(self):
        """Return rule as string representation."""
        return "{}: {}".format(self.rule_id, self.description)

    def __call__(self, *args, **kwargs):
        """Handle Rule objects as callables.

        When calling a rule, it is evaluated over (a part of) the bibliography.
        :param args, kwargs: Rule arguments
        :return: True if the bibliography is consistent with the rule, False if
        the rule is violated.
        """
        return self._rule(*args, **kwargs)

    @property
    def enabled(self):
        """Evaluate wheter a rule should be checked this run.

        :return: True if the rule should be checked based on the configuration
        used for running the linter, False otherwise
        """
        if get_config()['select']:
            for pattern in get_config()['select']:
                if fnmatch.fnmatch(self.rule_id, pattern):
                    return True
            return False
        if get_config()['ignore']:
            for pattern in get_config()['ignore']:
                if fnmatch.fnmatch(self.rule_id, pattern):
                    return False
            return True
        return True


class EntryRule(Rule):
    """Rule type evaluating a parsed bibliography entry."""

    def __init__(self, rule_id, description,
                 rule: Callable[[str, Entry, Dict[str, Entry]], bool]):
        """Create EntryRule object.

        :param key: The key of the current bibliography entry
        :param entry: The current bibliography entry
        :param database: All bibliography entries
        """
        super().__init__(rule_id, description, rule)


class TextRule(Rule):
    """Rule type evaluating a text line in the bibliography entry."""

    def __init__(self, rule_id, description,
                 rule: Callable[[int, str, str], bool]):
        """Create TextRule object.

        :param line_number: The number of the current line in the bibliography
        :param line: The content of the current line in the bibliography
        :param text: The entire bibliography
        """
        super().__init__(rule_id, description, rule)


class RuleStore:
    """Container for all loaded rules."""

    def __init__(self):
        """Create RuleStore object."""
        self._rules = []

    def register(self, rule: Rule):
        """Register a new rule.

        :param: a Rule object to register
        """
        position = 0
        while position < len(self._rules) \
                and self._rules[position].rule_id < rule.rule_id:
            position += 1
        self._rules.insert(position, rule)

    @property
    def all(self) -> List[Rule]:
        """Return all loaded rules."""
        return self._rules

    @property
    def enabled(self) -> List[Rule]:
        """Return all loaded rules enabled by the configuration."""
        return [rule for rule in self._rules if rule.enabled]

    @property
    def enabled_entry_rules(self) -> List[EntryRule]:
        """Return all loaded entry rules."""
        return [rule for rule in self.enabled if isinstance(rule, EntryRule)]

    @property
    def enabled_text_rules(self) -> List[TextRule]:
        """Return all loaded text rules."""
        return [rule for rule in self.enabled if isinstance(rule, TextRule)]


_ALL_RULES: RuleStore = RuleStore()


def register_entry_rule(rule_id, description: str) -> Callable:
    """Register a function as an entry rule."""
    def decorator(f: Callable[[str, Entry, Dict[str, Entry]], bool]):
        rule = EntryRule(rule_id, description, f)
        _ALL_RULES.register(rule)
    return decorator


def register_text_rule(rule_id: str, description: str) -> Callable:
    """Register a function as a text rule."""
    def decorator(f: Callable[[int, str, str], bool]):
        rule = TextRule(rule_id, description, f)
        _ALL_RULES.register(rule)
    return decorator


def load_rules() -> RuleStore:
    """Import all modules in the `bibla/rules` package."""
    for module in os.listdir(os.path.join(os.path.dirname(__file__), 'rules')):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        __import__('bibla.rules.' + module[:-3], locals(), globals())
    del module
    return _ALL_RULES

import logging
import re
import sys
from dataclasses import dataclass

from pybtex.database import parse_file

from bibl.rule import load_rules, Rule
from bibl.text_utils import find_entry_line_number, MONTH_NAMES

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.WARNING)
logger.addHandler(handler)


def lint(bibliography, output=True):
    bib_data = parse_file(bibliography, macros=MONTH_NAMES)
    bib_data.file = bibliography
    with open(bibliography, 'r') as bib_file:
        bib_text = bib_file.read()

    rules = load_rules()

    warnings = []

    _apply_text_rules(bibliography, bib_text, rules.enabled_text_rules, warnings)
    _apply_entry_rules(bibliography, bib_data, bib_text, rules.enabled_entry_rules, warnings)

    warnings.sort(key=lambda w: w.rule.id)
    warnings.sort(key=lambda w: w.line)
    if output:
        for warning in warnings:
            warning.log()
    return warnings


def _apply_text_rules(bibliography, bib_text, text_rules, warnings):
    for i, line in enumerate(bib_text.split('\n')):
        line_number = i + 1
        for rule in text_rules:
            result = rule(line_number, line, bib_text)
            if not result:
                warnings.append(LintWarning(bibliography, line_number, rule))


def _apply_entry_rules(bibliography, bib_data, bib_text, entry_rules, warnings):
    for key, entry in bib_data.entries.items():
        for rule in entry_rules:
            line_number, offset = find_entry_line_number(bib_text, key)
            result = rule(key, entry, bib_data)
            if not result:
                warnings.append(LintWarning(bibliography, line_number, rule))


@dataclass
class LintWarning:
    file: str
    line: int
    rule: Rule

    def log(self):
        msg = "{}:{} {}".format(self.file, self.line, str(self.rule))
        logger.warning(msg)

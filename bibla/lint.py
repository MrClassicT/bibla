"""Main linter logic."""
import logging
import sys
from dataclasses import dataclass
from typing import List, Iterable
from pybtex.database import BibliographyDataError
import re

import pybtex
from pybtex.database import parse_file
from bibla.rule import load_rules, Rule, EntryRule, TextRule
from bibla.text_utils import find_entry_line_number, MONTH_NAMES

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.WARNING)
logger.addHandler(handler)


@dataclass
class LintWarning:
    """Dataclass to represent and report a linter rule violation."""

    # file path of the detected violation
    file: str
    # line number of the detected violation
    line: int
    # the violated rule
    rule: Rule

    def log(self):
        """Print the warning with details to stdout."""
        msg = "{}:{} {}".format(self.file, self.line, str(self.rule))
        logger.warning(msg)


def lint(bibliography: str, verbose: bool = True) -> List[LintWarning]:
    """Execute the main linter program.

    The linter will first scan the bibliography text file and check all text
    rules for each line in the text file. Next, the file will be parsed by the
    pybtex parser and all entry rules will be checked.

    :param bibliography: a .bib bibliography file path
    :param verbose: log linter warnings to stdout
    :return: a list of LintWarning objects representing the linter violations
    found while running
    """
    try:
        bib_data = parse_file(bibliography, macros=MONTH_NAMES)
    except BibliographyDataError as e:
        # Extract the key from the error message
        match = re.search(r'repeated bibliograhpy entry: (.*)', str(e))
        if match:
            duplicate_key = match.group(1)
            print(f"{bibliography} D03: Duplicate entry with key '{duplicate_key}'")
        else:
            print(f"Warning: {e}")
        return []
    except pybtex.scanner.TokenRequired as e:
        print(f"E00: {e}. Make sure the file does not contain any comments by using '%'. Currently this is not supported due to the pybtex parser.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

    bib_data.file = bibliography
    with open(bibliography, 'r', encoding='utf-8') as bib_file:
        bib_text = bib_file.read()

    rules = load_rules()

    text_warnings = _apply_text_rules(bibliography, bib_text,
                                      rules.enabled_text_rules)
    entry_warnings = _apply_entry_rules(bibliography, bib_data, bib_text,
                                        rules.enabled_entry_rules)

    warnings = text_warnings + entry_warnings

    warnings.sort(key=lambda w: w.rule.rule_id)
    warnings.sort(key=lambda w: w.line)
    if verbose:
        for warning in warnings:
            warning.log()
    return warnings


def _apply_text_rules(bibliography: str, bib_text: str,
                      text_rules: Iterable[TextRule]) -> List[LintWarning]:
    """Check all text rules in the bibliography text file.

    :param bibliography: bibliography file path
    :param bib_text: bibliography file contents
    :param text_rules: list of text rules to be evaluated on each line of
    the file
    :return: a list of LinterWarnings representing found rule violations
    """
    warnings = []
    for i, line in enumerate(bib_text.split('\n')):
        line_number = i + 1
        for rule in text_rules:
            result = rule(line_number, line, bib_text)
            if not result:
                warnings.append(LintWarning(bibliography, line_number, rule))
    return warnings


def _apply_entry_rules(bibliography: str,
                       bib_data: pybtex.database.BibliographyData,
                       bib_text: str, entry_rules: Iterable[EntryRule]) \
        -> List[LintWarning]:
    """Check all entry rules in the bibliography text file.

    :param bibliography: bibliography file path
    :param bib_data: parsed bibliography data containing entries
    :param bib_text: bibliography file contents
    :param text_rules: list of text rules to be evaluated on each line of
    the file
    :return: a list of LinterWarnings representing found rule violations
    """
    warnings = []
    for key, entry in bib_data.entries.items():
        for rule in entry_rules:
            line_number, offset = find_entry_line_number(bib_text, key)
            result = rule(key, entry, bib_data)
            if not result:
                warnings.append(LintWarning(bibliography, line_number, rule))
    return warnings

import logging
import re
import sys

from pybtex.database import parse_file

from bibl.rule import load_entry_rules
from bibl.text_utils import find_entry_line_number


def bibl(bibliography, config=None):
    bib_data = parse_file(bibliography)
    bib_data.file = bibliography
    with open(bibliography, 'r') as bib_file:
        bib_text = bib_file.read()
    entry_rules = load_entry_rules()
    num_warnings = 0
    for key, entry in bib_data.entries.items():
        for id, rule in entry_rules.enabled.items():
            line_number, offset = find_entry_line_number(bib_text, key)
            result = rule(key, entry, bib_data)
            if not result:
                lint_warning(line_number, offset, rule)
                num_warnings += 1
    if num_warnings > 0:
        sys.exit(1)


def lint_warning(line_number, offset, rule):
    logger = logging.getLogger()
    msg = "Line {}:{} {} {}".format(line_number, offset, rule.id, rule.description)
    logger.warning(msg)

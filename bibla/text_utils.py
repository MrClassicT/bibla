"""Text processing helper functions for linter rules and bibla commands."""

import re
from typing import List

import markdown_table

# Month name dictionary for pybtex
from bibla.rule import Rule

MONTH_NAMES = {
    'jan': 'jan',
    'feb': 'feb',
    'mar': 'mar',
    'apr': 'apr',
    'may': 'may',
    'jun': 'jun',
    'jul': 'jul',
    'aug': 'aug',
    'sep': 'sep',
    'oct': 'oct',
    'nov': 'nov',
    'dec': 'dec'
}


def find_match_line_number(text: str, pattern: str, group: int) -> (int, int):
    r"""Find the line number and offset of a regex match.

    :param text: text to match
    :param pattern: regex pattern
    :param group: regex group number of the intended match
    :return: Line number (based on \n characters) of first occurrence of the
    specified match, offset of the first occurrence of the match in the line
    """
    regex = re.compile(pattern)
    try:
        match = next(regex.finditer(text))
    except StopIteration:
        return 0, 0
    start = match.start(group)
    lineno = text.count('\n', 0, start)
    if lineno:
        offset = start - text.rfind('\n', 0, start)
    else:
        offset = start
    return lineno + 1, offset + 1


def find_entry_line_number(text: str, key: str) -> (int, int):
    r"""Find the file line number of a pybtex entry.

    :param text: biblatex file string
    :param key: Entry key
    :return: Line number (based on \n characters) of first occurrence of the
    entry key, offset of the first occurrence of the key in the line
    """
    pattern = r'\s*@[a-zA-Z]+\s*{\s*(' + key + r')\s*,'
    return find_match_line_number(text, pattern, 1)


def format_rules_markdown_tables(rules: List[Rule]) -> str:
    """Format a list of bibla rules as a Markdown table.

    :param: rules: a list of Rule instances
    :return: A string containing a markdown table of human readable rules
    """
    result = "# bibla rules\n"
    headers = ["Rule ID", "Rule description"]
    matrix = []
    for i, rule in enumerate(rules):
        if i != 0 and rule.rule_id[0] != rules[i - 1].rule_id[0]:
            result += "## " + rules[i - 1].rule_id[0]
            result += "\n"
            result += markdown_table.render(headers, matrix)
            result += "\n\n"
            matrix = []
        matrix.append([f'`{rule.rule_id}`', rule.description])
    result += "## " + rule.rule_id[0]
    result += "\n"
    result += markdown_table.render(headers, matrix)
    return result

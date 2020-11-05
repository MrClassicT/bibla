import re

import markdown_table

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


def find_match_line_number(text, pattern, group):
    regex = re.compile(pattern)
    match = next(regex.finditer(text))
    start = match.start(group)
    lineno = text.count('\n', 0, start)
    if lineno:
        offset = start - text.rfind('\n', 0, start)
    else:
        offset = start
    return lineno + 1, offset + 1


def find_entry_line_number(text, key):
    pattern = r'\s*@[a-zA-Z]+\s*{\s*(' + key + ')\s*,'
    return find_match_line_number(text, pattern, 1)


def format_rules_markdown_tables(rules):
    result = "# bibL rules\n"
    headers = ["Rule ID", "Rule description"]
    matrix = []
    for i, rule in enumerate(rules):
        if i != 0 and rule.id[0] != rules[i - 1].id[0]:
            result += "## " + rules[i - 1].id[0]
            result += "\n"
            result += markdown_table.render(headers, matrix)
            result += "\n\n"
            matrix = []
        matrix.append([f'`{rule.id}`', rule.description])
    result += "## " + rule.id[0]
    result += "\n"
    result += markdown_table.render(headers, matrix)
    return result

import re

def find_match_line_number(text, pattern, group):
    regex = re.compile(pattern)
    match = next(regex.finditer(text))
    start = match.start(group)
    lineno = text.count('\n', 0, start)
    if lineno:
        offset = start - text.rfind('\n', 0, start)
    else:
        offset = start
    return lineno+1, offset+1


def find_entry_line_number(text, key):
    pattern = r'\s*@[a-zA-Z]+\s*{\s*(' + key + ')\s*,'
    return find_match_line_number(text, pattern, 1)

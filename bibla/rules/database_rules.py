"""Linter rules checking the consistency of the entire BibLaTeX file."""
import re
from fuzzywuzzy import fuzz
from unidecode import unidecode
from bibla.rule import register_entry_rule, register_text_rule


@register_entry_rule('D00', 'Entry not in alphabetical order by key')
def keys_alphabetical(key, entry, database):
    """Raise a linter warning when entries are not in alphabetical order by key.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if the key of the current entry is alphabetically larger than
    or equal to the key of the previous entry, False otherwise.
    """
    keys = list(database.entries.keys())
    entry_num = keys.index(key)
    if entry_num == len(keys) - 1:
        return True
    else:
        return entry.key.lower() <= keys[entry_num + 1].lower()


@register_text_rule('D01', 'Preamble should begin at first line of document')
def line_length(line_number, line, text):
    """Raise a linter warning when the preamble is not on the first line.

    :param line_number: The number of the current line in the bibliography
    :param line: The content of the current line in the bibliography
    :param text: The entire bibliography
    :return: True if no preamble is present or the preambel starts at line 1 of
    the biblatex file, False otherwise.
    """
    regex = re.compile(r'^\s*@preamble')
    return not regex.match(line.lower()) or line_number == 0


@register_entry_rule('D02', 'Possible duplicate entry based on similar titles')
def title_duplicate(key, entry, database):
    """Raise a linter warning when entries with a similar titles are present.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if the fuzzy match partial ratio of the title of the current
    entry with any other entry exceeds 90%, False otherwise.
    """
    if 'title' not in entry.fields:
        return True
    for e in database.entries.values():
        if 'title' not in e.fields:
            continue
        t1 = unidecode(entry.fields['title']).lower()
        t2 = unidecode(e.fields['title']).lower()
        if e != entry and fuzz.partial_ratio(t1, t2) > 90:
            return False
    return True

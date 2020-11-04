import re

from fuzzywuzzy import fuzz
from unidecode import unidecode

from bibl.rule import register_entry_rule, register_text_rule



@register_entry_rule('D00', 'Entry not in alphabetical order by key')
def keys_alphabetical(key, entry, database):

    keys = list(database.entries.keys())
    entry_num = keys.index(key)
    if entry_num == len(keys) -1:
        return True
    else:
        return entry.key.lower() <= keys[entry_num+1].lower()

@register_text_rule('D01', 'Preamble should begin at first line of document')
def line_length(line_number, line, text):
    regex = re.compile(r'^\s*@preamble')
    return not regex.match(line.lower()) or line_number == 0

# TODO: check fuzzy author name consistency


# TODO fuzzy match on entire entry
@register_entry_rule('D02', 'Possible duplicate entry based on similar titles')
def title_duplicate(key, entry, database):
    if not 'title' in entry.fields:
        return True
    for e in database.entries.values():
        if not 'title' in e.fields:
            continue
        t1 = unidecode(entry.fields['title']).lower()
        t2 = unidecode(e.fields['title']).lower()
        if e != entry and fuzz.partial_ratio(t1, t2) > 90:
            return False
    return True

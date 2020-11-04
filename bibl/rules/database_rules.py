import re

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

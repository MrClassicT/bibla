import itertools
import os
import re
from unidecode import unidecode
from bibl.rule import register_entry_rule
import yaml

with open(os.path.join(os.path.dirname(__file__), 'type_spec.yml')) as type_spec_file:
    TYPES = yaml.load(type_spec_file, Loader=yaml.FullLoader)


@register_entry_rule('E00', 'Unrecognized entry type')
def E00(key, entry, database):
    return entry.type in TYPES.keys()


@register_entry_rule('E01', 'Keys of published works should have format AuthorYEARa')
def E01(key, entry, database):
    if not 'year' in entry.fields:
        return True
    author = entry.persons['author'][0]
    names = author.rich_prelast_names + author.rich_last_names
    correct_key_unicode = "".join([str(name.capitalize()) for name in names]) + entry.fields['year']
    correct_key_ascii = unidecode(correct_key_unicode)
    regex = re.compile(correct_key_ascii + r'[a-zA-Z]?')
    return bool(regex.match(key))


@register_entry_rule('E02', 'Possible duplicate entry based on title')
def E02(key, entry, database):
    if not 'title' in entry.fields:
        return True
    for e in database.entries.values():
        if not 'title' in e.fields:
            continue
        t1 = unidecode(entry.fields['title']).lower()
        t2 = unidecode(e.fields['title']).lower()
        if t1 == t2 and e != entry:
            return False
    return True


@register_entry_rule('E03', 'Author first names should not be abbreviated')
def E03(key, entry, database):
    for person in itertools.chain(*entry.persons.values()):
        for name in person.first_names:
            if len(name) == 1:
                return False
    return True


@register_entry_rule('E04', 'Author middle names should be abbreviated with .')
def E04(key, entry, database):
    for person in itertools.chain(*entry.persons.values()):
        for name in person.middle_names:
            if len(name) == 1:
                return False
    return True

def _process_file_path(file):
    if ':' in file:
        return file.split(':')[1]
    else:
        return file


@register_entry_rule('E05', 'Files should be linked with relative path')
def E05(key, entry, database):
    if 'file' in entry.fields:
        path = _process_file_path(entry.fields['file'])
        return not os.path.isabs(path)
    else:
        return True


@register_entry_rule('E06', 'Linked file is not present')
def E06(key, entry, database):
    if 'file' in entry.fields:
        path = _process_file_path(entry.fields['file'])
        if os.path.isabs(path):
            return os.path.exists(path)
        else:
            abs_path = os.path.join(os.path.dirname(database.file), path)
            return os.path.exists(abs_path)
    else:
        return True



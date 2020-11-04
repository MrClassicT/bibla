import itertools
import os
import re
from unidecode import unidecode

from bibl.config import get_config
from bibl.rule import register_entry_rule
from bibl.text_utils import MONTH_NAMES


# TODO: use of undefined symbol



@register_entry_rule('E00', 'Keys of published works should have format AuthorYEARa')
def key_format(key, entry, database):
    if not 'year' in entry.fields:
        return True
    author = entry.persons['author'][0]
    names = author.rich_prelast_names + author.rich_last_names
    correct_key_unicode = "".join([str(name.capitalize()) for name in names]) + entry.fields['year']
    correct_key_ascii = unidecode(correct_key_unicode)
    regex = re.compile(correct_key_ascii + r'[a-zA-Z]?')
    return bool(regex.match(key))


@register_entry_rule('E01', f'Author first names should not be abbreviated')
def author_first_name_abbr(key, entry, database):
    for person in itertools.chain(*entry.persons.values()):
        for name in person.first_names:
            if len(name) == 1:
                return False
    return True


if get_config()['abbreviation_dot']:
    author_middle_name_abbr_desc = "Author middle names should be abbreviated with ."
else:
    author_middle_name_abbr_desc = "Author middle names should be abbreviated without ."


@register_entry_rule('E02', author_middle_name_abbr_desc)
def author_middle_name_abbr(key, entry, database):
    for person in itertools.chain(*entry.persons.values()):
        for name in person.middle_names:
            if get_config()['abbreviation_dot'] and len(name) == 1:
                return False
            if not get_config()['abbreviation_dot'] and name.endswith('.'):
                return False
    return True


@register_entry_rule('E03', 'The usage of `et al.` in the author field should be replaced by a list of all authors')
def author_et_al(key, entry, database):
    if 'author' in entry.fields:
        return not entry.fields['author'].lower().contains('et al')
    else:
        return True


def _process_file_path(file):
    if ':' in file:
        return file.split(':')[1]
    else:
        return file


@register_entry_rule('E04', 'Files should be linked with relative path')
def file_relative_path(key, entry, database):
    if 'file' in entry.fields:
        path = _process_file_path(entry.fields['file'])
        return not os.path.isabs(path)
    else:
        return True


@register_entry_rule('E05', 'Linked file is not present')
def file_present(key, entry, database):
    if 'file' in entry.fields:
        path = _process_file_path(entry.fields['file'])
        if os.path.isabs(path):
            return os.path.exists(path)
        else:
            abs_path = os.path.join(os.path.dirname(database.file), path)
            return os.path.exists(abs_path)
    else:
        return True


@register_entry_rule('E06', 'Incorrect doi format')
def doi_format(key, entry, database):
    if 'doi' in entry.fields:
        regex = re.compile(r'^10.\d{4,9}/[-._;()/:a-z0-9]+$')
        return bool(regex.match(entry.fields['doi']))
    else:
        return True


@register_entry_rule('E07', 'Incorrect ISBN format')
def isbn_format(key, entry, database):
    if 'isbn' in entry.fields:
        regex = re.compile(r'^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$')
        return bool(regex.match(entry.fields['isbn']))
    else:
        return True


@register_entry_rule('E08', 'Page numbers should have format xx--yy')
def page_format(key, entry, database):
    if 'page' in entry.fields:
        regex = re.compile(r'^\d+(--\d+)?$')
        return bool(regex.match(entry.fields['page']))
    else:
        return True


@register_entry_rule('E09', 'End page larger than start page. Page numbers in aaaa--bb should be written as aaaa--aabb')
def page_format_ascending(key, entry, database):
    if 'page' in entry.fields:
        regex = re.compile(r'^\d+--\d+$')
        if not regex.match(entry.fields['page']):
            return True
        else:
            groups = entry.fields['page'].split('--')
            return int(groups[1]) >= int(groups[0])
    else:
        return True


@register_entry_rule('E10', 'Month should be in 3-letter lowercase format')
def month_format(key, entry, database):
    if 'month' in entry.fields:
        return entry.fields['month'] in MONTH_NAMES.keys()
    else:
        return True

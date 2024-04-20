"""Linter rules checking the format and consistency of field values."""

import itertools
import os
import re
from unidecode import unidecode

from bibla.config import get_config
from bibla.rule import register_entry_rule
from bibla.text_utils import MONTH_NAMES


# TODO: use of undefined string


@register_entry_rule(
    'E00',
    'Keys of published works should have format `AuthorYEARa`')
def key_format(key, entry, database):
    """Raise a linter warning when entry key is not of format `AuthorYEARa`.

    E.g. an entry with values
    ```
    author = {Arthur B Cummings and David Eftekhary and Frank G House},
    year   = {2003}
    ```
    should have key `Cummings2003`.
    If another entry with the same year and main author is present,
    their keys should have formats `Cummings2003a` and `Cummings2003b`.
    This rule only applies when `year` and at least one author are set.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if the current entry's key has the specified format or
    year or author are not specified, False otherwise.
    """
    if 'year' not in entry.fields or list(
            itertools.chain(*entry.persons.values())):
        return True
    author = entry.persons['author'][0]
    names = author.rich_prelast_names + author.rich_last_names
    correct_key_unicode = "".join([str(name) for name in names]) + \
                          entry.fields['year']
    correct_key_ascii = unidecode(correct_key_unicode)
    regex = re.compile(correct_key_ascii + r'[a-zA-Z]?')
    return bool(regex.match(key))


@register_entry_rule('E01', 'Author first names should not be abbreviated')
def author_first_name_abbr(key, entry, database):
    """Raise a linter warning when an author/editor first name is abbreviated.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if none of the first names of authors or editors are
    abbreviated, False otherwise.
    """
    for person in itertools.chain(*entry.persons.values()):
        for name in person.first_names:
            if len(name) == 1:
                return False
    return True


if get_config()['abbreviation_dot']:
    middlename_abbr_desc = "Author middle names should be abbreviated with ."
else:
    middlename_abbr_desc = "Author middle names should be abbreviated without."


@register_entry_rule('E02', middlename_abbr_desc)
def author_middle_name_abbr(key, entry, database):
    """Raise a linter warning when a middle name is inconsistently abbreviated.

    The configuration setting `abbreviation_dot` determines whether all
    person middle names should be abbreviated with a trailing dot
    (e.g. John F. Kennedy) or without (e.g. John F Kennedy).
    Depending on the value of this setting, a warning will be raised if the
    current entry contains a person middle that is incorrectly formatted.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: If `abbreviation_dot` is True:
        True if all middle names of persons in the current entry are
        abbreviated with a period, False otherwise.
    If `abbreviation_dot` is False:
        True if all middle names of persons in the current entry are
        abbreviated without a period, False otherwise.
    """
    for person in itertools.chain(*entry.persons.values()):
        for name in person.middle_names:
            if get_config()['abbreviation_dot'] and len(name) == 1:
                return False
            if not get_config()['abbreviation_dot'] and name.endswith('.'):
                return False
    return True


@register_entry_rule(
    'E03',
    'The usage of `et al.` in the author field should be replaced by a list '
    'of all authors')
def author_et_al(key, entry, database):
    """Raise a linter warning when the authors or editors contains 'et al.'.

    Authors and editors should be specifed as a complete list of all names.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if none of the author or editor names of the current entry
    contains the substring 'et al' (case insensitive), False otherwise.
    """
    if 'author' not in entry.fields:
        return True
    return not entry.fields['author'].lower().contains('et al')


def _process_file_path(file):
    if ':' in file:
        return file.split(':')[1]
    return file


@register_entry_rule('E04', 'Files should be linked with relative path')
def file_relative_path(key, entry, database):
    """Raise a linter warning when a file field value is an absolute path.

    If the optional `file` field is present, its value should be a file path
    relative to the current bibliography file location.
    OS style file paths and JabRef file paths are accepted as `file` values.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if the `file` field is not present in the current entry or
    the path specified in `file` is relative, False otherwise.
    """
    if 'file' not in entry.fields:
        return True
    path = _process_file_path(entry.fields['file'])
    return not os.path.isabs(path)


@register_entry_rule('E05', 'Linked file is not present')
def file_present(key, entry, database):
    """Raise a linter warning when a linked file is not found on the machine.

    Relative paths are evaluated from the directory of the current
    bibliography file.
    OS style file paths and JabRef file paths are accepted as `file` values.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if the `file` field is not present in the current entry or
    a file exists at the path specified in `file`, False otherwise.
    """
    if 'file' not in entry.fields:
        return True
    path = _process_file_path(entry.fields['file'])
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(database.file), path)
    return os.path.exists(path)


@register_entry_rule('E06', 'Incorrect doi format')
def doi_format(key, entry, database):
    """Raise a linter warning when a DOI field is incorrectly formatted.

    DOIs should be specified starting as `doi:.../...`,
    e.g. `doi:10.1038/nphys1170`, and not as an url starting with
    `http://doi.org...`.
    DOI regex from  https://www.crossref.org/blog/dois-and-matching-regular
    -expressions/.
    This regex is not exact and sometimes fails, since DOIs are flexible.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if the current entry does not contain a `doi` field or the
    value of the `doi` field matches the DOI regex, False otherwise.
    """
    if 'doi' not in entry.fields:
        return True
    doi_regex = r'^10.\d{4,9}/[-._;()/:a-z0-9]+$'
    regex = re.compile(doi_regex)
    return bool(regex.match(entry.fields['doi']))


@register_entry_rule('E07', 'Incorrect ISBN format')
def isbn_format(key, entry, database):
    """Raise a linter warning when an ISBN field is incorrectly formatted.

    Accepts ISBN-10 and ISBN-13 formats.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if the current entry does not contain an `isbn` field or the
    value of the `isbn` field mathches the ISBN regex, False otherwise.
    """
    if 'isbn' not in entry.fields:
        return True
    isbn_regex = r'^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$'
    regex = re.compile(isbn_regex)
    return bool(regex.match(entry.fields['isbn']))


@register_entry_rule(
    'E08',
    'End page larger than start page. Page numbers in '
    'aaaa--bb should be written as aaaa--aabb')
def page_format_ascending(key, entry, database):
    """Raise a linter warning when large page numbers are abbreviated.

    Page numbers where only the changing digit of the ending page are displayed
    should be written in full, e.g. 1234--1256 instead of 1234--56.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return:True if the current entry does not contain a page field, the page
    field only has one page number or the page field is not abbreviated, False
    when the page field is abbreviated or the ending page number is larger than
    the starting page number.
    """
    if 'page' not in entry.fields:
        return True
    page_regex = r'^\d+--\d+$'
    regex = re.compile(page_regex)
    if not regex.match(entry.fields['page']):
        return True
    groups = entry.fields['page'].split('--')
    if len(groups) <= 1:
        return True
    return int(groups[1]) >= int(groups[0])


@register_entry_rule('E09', 'Month should be in 3-letter lowercase format')
def month_format(key, entry, database):
    """Raise a linter warning when the month name is incorrectly abbreviated.

    Following month codes are accepted:
        jan
        feb
        mar
        apr
        may
        jun
        jul
        aug
        sep
        oct
        nof

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if no month is present or the month is correctly abbreviated,
    False otherwise.
    """
    if 'month' not in entry.fields:
        return True
    return entry.fields['month'] in MONTH_NAMES.keys()
"""Linter rules checking the format and consistency of field values."""

import itertools
import os
import re
from unidecode import unidecode

from bibla.config import get_config
from bibla.rule import register_entry_rule


@register_entry_rule('E00', 'Keys of published works should have format `AuthorYEARa`')
def key_format(key, entry, database):
    """Raise a linter warning when entry key is not of format `AuthorYEARa`.

    E.g. an entry with values
    ```
    author = {Arthur B Cummings and David Eftekhary and Frank G House},
    date   = {2003-02-02}
    ```
    should have key `Cummings2003`.
    If another entry with the same year and main author is present,
    their keys should have formats `Cummings2003a` and `Cummings2003b`.
    This rule only applies when `date` and at least one author are set.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if the current entry's key has the specified format or
    year or author are not specified, False otherwise.
    """
    if 'date' not in entry.fields or len(entry.persons.get('author', [])) == 0:
        return True
    try:
        author = entry.persons['author'][0]
    except KeyError:
        try:
            author = entry.persons['editor'][0]
        except KeyError:
            return True
    names = author.rich_prelast_names + [name for last_name in author.rich_last_names for name in last_name.split('-')]
    date = entry.fields['date']
    year_match = re.search(r'\d{4}', date)
    if not year_match:
        return True  # Safely handle cases where no year is found, another error is responsible for this
    year = year_match.group()

    # Check for 'EtAl' in the key when there are more than 3 authors
    if len(entry.persons.get('author', [])) >= 3 and 'EtAl' in key.lower():
        correct_key_unicode = names[0] + 'EtAl' + year
    # Check for two names in the key when there are exactly 2 authors
    elif len(entry.persons.get('author', [])) == 2:
        correct_key_unicode = "".join([str(name) for name in names[:2]]) + year
    else:
        correct_key_unicode = "".join([str(name) for name in names]) + year

    correct_key_ascii = unidecode(str(correct_key_unicode))
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
        True if all middle names of people in the current entry are
        abbreviated with a period, False otherwise.
    If `abbreviation_dot` is False:
        True if all middle names of people in the current entry are
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
    '`pages` field formatting is incorrect. Please use the following format: 123--456. '
    'In ascending order seperated with two dashes.')
def page_format(key, entry, database):
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
    if 'pages' not in entry.fields:
        return True
    page_regex = r'^(\d+--\d+|\d+)(,(\d+--\d+|\d+))*$'
    regex = re.compile(page_regex)
    if not regex.match(entry.fields['pages']):
        return False
    
    pages = entry.fields['pages']
    page_numbers = re.findall(r'\d+', pages)
    page_numbers = [int(num) for num in page_numbers]
    
    if page_numbers != sorted(page_numbers):
        return False
    
    return True


@register_entry_rule('E09', 'Entry should use correct date format: YYYY-MM-DD, YYYY-MM or YYYY!')
def correct_date_format(key, entry, database):
    """Raise a linter warning when the date field does not have the correct format.

    Format must equal to: YYYY-MM-DD

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if no date is present or the date is correctly formatted,
    False otherwise.
    """
    if 'date' not in entry.fields:
        return True
    date = entry.fields['date']
    regex = re.compile(r'^(\d{4})-(\d{2})-(\d{2})$')
    match = regex.match(date)
    if not match:
        regex = re.compile(r'^(\d{4})-(\d{2})$')
        match = regex.match(date)
        if not match:
            regex = re.compile(r'^(\d{4})$')
            match = regex.match(date)
            if not match:
                return False
            return True
        year, month = map(int, match.groups())
        if not (1 <= month <= 12):
            return False
        return True
    year, month, day = map(int, match.groups())
    if not (1 <= month <= 12):
        return False
    if not (1 <= day <= 31):
        return False
    return True


def register_alternate_entry_type_rule(entry_type, alt_entry_type):
    rule_id = 'E11{}{}'.format(entry_type.capitalize(), alt_entry_type.capitalize())
    message = "`{}` is an alias, please use the original type `{}` instead.".format(alt_entry_type, entry_type)

    @register_entry_rule(rule_id, message)
    def check_alias_entry_type(key, entry, database, entry_type=entry_type, alt_entry_type=alt_entry_type):
        """Raise a linter warning when an alias entry type is used instead of the original one.

        This function checks if the entry type is an alias entry type.
        If it is, it suggests to use the preferred/original entry type instead.

        :param key: The key of the current bibliography entry
        :param entry: The current bibliography entry
        :param database: All bibliography entries
        :param entry_type: The preferred/original entry type
        :param alt_entry_type: The alias entry type
        :return: False if the alias entry type is used, True otherwise
        """
        if entry.type == alt_entry_type:
            return False
        else:
            return True


alias_entry_types = get_config().get('alias_entry_types', {})
for entry_type, alt_entry_types in alias_entry_types.items():
    for alt_entry_type in alt_entry_types:
        register_alternate_entry_type_rule(entry_type, alt_entry_type)


@register_entry_rule('E12', 'Homepages should not be used as a source')
def check_homepage_in_url(key, entry, database):
    """Raise a linter warning when a URL field contains a homepage.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if the URL field does not contain a homepage, False otherwise.
    """
    if 'url' not in entry.fields:
        return True
    url = entry.fields['url']
    regex = re.compile(r'^(https?://)?[^/]+/?$')
    if regex.match(url):
        return False
    return True


@register_entry_rule('E13', 'URLs should only include the critical parts and nothing more')
def check_url_directive_parts(key, entry, database):
    """Raise a linter warning when a URL field contains text highlighting directive parts.

    :param key: The key of the current bibliography entry
    :param entry: The current bibliography entry
    :param database: All bibliography entries
    :return: True if the URL field does not contain any text highlighting directive parts, False otherwise.
    """
    if 'url' not in entry.fields:
        return True
    url = entry.fields['url']
    if ('#' or '?' or '%') in url:
        return False
    return True

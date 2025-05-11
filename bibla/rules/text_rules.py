"""Linter rules checking the text lay-out of the bibliography file."""

import re

from bibla.config import get_config
from bibla.rule import register_text_rule

@register_text_rule('T01',
                    'Non-standard whitespace at beginning of line (indents '
                    'should be {} spaces)'
                    .format(get_config()['indent_spaces']))
def trailing_whitespace(line_number, line, text):
    """Raise a linter warning when a line starts with a non-standard indent.

    Valid indents are space characters in multiples of the indent defined in
    the configuration with the `indent_spaces`.
    This rule also raises a warning when a line starts with a whitespace
    character that is not a space.

    Invalid trailing whitespace characters are:
    * A tab character
    * A vertical tab character
    * A form feed character

    :param line_number: The number of the current line in the bibliography
    :param line: The content of the current line in the bibliography
    :param text: The entire bibliography
    :return: True if the current line does not start
    """
    regex = re.compile(
        r'(^ {' + str(get_config()['indent_spaces']) + r'}\S)|(^\S)|(^$)')
    return bool(regex.match(line))


@register_text_rule('T02', 'Whitespace at end of line')
def ending_whitespace(line_number, line, text):
    """Raise a linter warning when a line ends in a whitespace character.

    Whitespace characters are:
    * A space character
    * A tab character
    * A vertical tab character
    * A form feed character

    :param line_number: The number of the current line in the bibliography
    :param line: The content of the current line in the bibliography
    :param text: The entire bibliography
    :return: True if the current line des not end in whitespace,
    False otherwise.
    """
    regex = re.compile(r'(^.*\S$)|(^$)')
    return bool(regex.match(line))


@register_text_rule('T03', 'Line length exceeds {} characters'.format(
    get_config()['max_line_length']))
def line_length(line_number, line, text):
    """Raise a linter warning when a maximum line length is exceeded.

     The maximum line length is defined in the configuration with the
     `max_line_length` setting.

    :param line_number: The number of the current line in the bibliography
    :param line: The content of the current line in the bibliography
    :param text: The entire bibliography
    :return: True if the current line length is smaller or equal to the
    maximum number of characthers, False otherwise
    """
    return len(line) <= get_config()['max_line_length']

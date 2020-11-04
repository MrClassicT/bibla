import re

from bibl.config import get_config
from bibl.rule import register_text_rule


@register_text_rule('T00', 'Non-ascii character')
def ascii_chars(line_number, line, text):
    return line.isascii()


@register_text_rule('T01', 'Non-standard whitespace at beginning of line (indents should be {} spaces)'.format(
    get_config()['indent_spaces']))
def trailing_whitespace(line_number, line, text):
    regex = re.compile(r'(^ {' + str(get_config()['indent_spaces']) + r'}\S)|(^\S)|(^$)')
    return bool(regex.match(line))


@register_text_rule('T02', 'Whitespace at end of line')
def ending_whitespace(line_number, line, text):
    regex = re.compile(r'(^.*\S$)|(^$)')
    return bool(regex.match(line))


@register_text_rule('T03', 'Line length exceeds {} characters'.format(get_config()['max_line_length']))
def line_length(line_number, line, text):
    return len(line) <= get_config()['max_line_length']

# TODO: invalid syntax
# TODO: preamble first line
# TODO: string directly after preamble

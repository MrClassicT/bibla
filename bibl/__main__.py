import os
import warnings

import click
from bibl import __version__
from bibl.lint import lint as bibl_lint
from bibl.config import load_config_file, set_config
from bibl.rule import load_rules
from bibl.text_utils import format_rules_markdown_tables


@click.group()
@click.option('-c', '--config', help='Custom configuration file path.', type=str)
@click.option('--select', help='Comma separated list of enabled rules, all other rules will be disabled.', type=str)
@click.option('--ignore', help='Comma separated list of disabled rules, all other rules will be enabled.', type=str)
@click.option('--indent-spaces', help='Number of trailing whitespaces for indented line, used by TO1.', type=int)
@click.option('--max-line-length', help='Max line length before wrap recommended, used by T03.', type=int)
def cli(config, select, ignore, indent_spaces, max_line_length):
    if not config is None:
        load_config_file(config)
    elif os.path.isfile('.bibl.yml'):
        load_config_file('.bibl.yml')

    if not select is None:
        set_config('select', select.split(','))
    if not ignore is None:
        set_config('ignore', ignore.split(','))
    set_config('indent_spaces', indent_spaces)
    set_config('max_line_length', max_line_length)


@cli.command(help="Lint a BibTeX bibliography file.")
@click.argument('bibliography', type=str, nargs=-1)
def lint(bibliography):
    warnings.filterwarnings("ignore")
    for bib in bibliography:
        bibl_lint(bib)


@cli.command(help="Show all available rules.")
@click.option('-m', 'markdown', help='Format rules as markdown table.', is_flag=True)
def list_all(markdown):
    rules = load_rules().all
    if markdown:
        click.echo(format_rules_markdown_tables(rules))
    else:
        for rule in rules:
            click.echo(rule)


@cli.command(help="Show all rules enabled by the configuration.")
@click.option('-m', 'markdown', help='Format rules as markdown table.', is_flag=True)
def list_enabled(markdown):
    rules = load_rules().enabled
    if markdown:
        click.echo(format_rules_markdown_tables(rules))
    else:
        for rule in rules:
            click.echo(rule)

@cli.command(help="Show the package version.")
def version():
    click.echo('bibL version: ' + __version__)

if __name__ == '__main__':
    cli(prog_name='bibl')

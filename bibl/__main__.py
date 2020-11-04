import click
from bibl.lint import lint as bibl_lint
from bibl.config import load_config
from bibl.rule import load_rules
from bibl.text_utils import format_rules_markdown_tables


@click.group()
@click.option('-c', '--config', default='.bibl.yml', help='Custom configuration file path.', type=str)
def cli(config):
    load_config(config)


@cli.command(help="Lint a BibTeX bibliography file.")
@click.argument('bibliography', type=str)
def lint(bibliography):
    bibl_lint(bibliography)


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


if __name__ == '__main__':
    cli(prog_name='python -m bibl')

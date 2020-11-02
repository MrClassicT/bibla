import click

from bibl.lint import bibl


@click.command()
@click.argument('bibliography')
@click.option('--config', default='.bibl', help='configuration file path')
def bibl_cli(bibliography, config):
    bibl(bibliography, config)


if __name__ == '__main__':
    bibl_cli()

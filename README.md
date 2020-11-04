# bibl

bibl is a minimalistic linter for BibTeX files.
bibl does not come with its own BibTeX parser, but leverages the [pybtex](https://pybtex.org/) parser.

## Installation

```shell script
pip install git+https://gitlab.com/arne.vandenkerchove/biblint.git
```
## Usage

### Command
```shell script
Usage: bibl [OPTIONS] COMMAND [ARGS]...

Options:
  -c, --config TEXT          Custom configuration file path.
  --select TEXT              Comma separated list of enabled rules, all other
                             rules will be disabled.

  --ignore TEXT              Comma separated list of disabled rules, all other
                             rules will be enabled.

  --indent-spaces INTEGER    Number of trailing whitespaces for indented line,
                             used by TO1.

  --max-line-length INTEGER  Max line length before wrap recommended, used by
                             T03.

  --abbreviation-dot         Abbreviate middle names with dot.
  --help                     Show this message and exit.

Commands:
  lint          Lint a BibTeX bibliography file.
  list-all      Show all available rules.
  list-enabled  Show all rules enabled by the configuration.
```

```shell script
bibl --ignore "F01*,E07,D0*" lint bibliography.lint 
```

### Rules

## Configuration
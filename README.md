# bibL

bibL is a minimalistic linter (style checker) for BibTeX files.
bibL does not come with its own BibTeX parser, but leverages the [pybtex](https://pybtex.org/) parser.

## Installation

```shell script
pip install bibl
```
## Usage

Run bibl on your BibTeX files with the following command
```shell script
bibl lint bibliography1.bib bibliography2.bib ... 
```
or as a python module with
```shell script
python -m bibl lint bibliography1.bib bibliography2.bib ... 
```

bibl will check these files for a variety of style issues and deviations from the BibTeX spec (http://www.bibtex.org/Format/, https://en.wikipedia.org/wiki/BibTeX).
Each possible type of issue is formulated as a rule. Each rule is identified by a unique code. Some examples of rules are 

Rule ID|Rule description
-|-
`D00`|Entry not in alphabetical order by ke
`T00`|Non-ascii character
`E00`|Keys of published works should have format AuthorYEARa
`E06`|Incorrect doi format
`T01`|Non-standard whitespace at beginning of line (indents should be 4 spaces)
`M01ArticleYear`|Missing required field `year` for entry type `article`
...|...

This link provides a [list of all available rules](http://gitlab.com/arne.vandenkerchove/bibl/-/jobs/artifacts/master/file/all_rules.html?job=rule_list)


The first character of a rule id refers to a rules category, e.g. `E` for issues with entry values, `T` for textual
issues with the `.bib` file, etc.
You can specify which rules to check by using `--select` or `--ignore`. Wildcards are allowed. `--select` will only
enable the specified rules, disabling all other rules, while `--ignore` will disable all rules except the ones specified.
`--select` and `--ignore` may not be specified simultaneously.
```shell script
bibl --select "D*,E06,T01" lint bibliography.lint
```
will only check all rules starting with D, rule E06 and rule T01
```
bibl --ignore "D*,E06,T01" lint bibliography.lint
```
will check all rules except all rules starting with D, rule E06 and rule T01

## Configuration

Aside from `--select` and `--ignore`, other configuration options can be provided via the cli, like `--max-line-length`
to specify the line length for which an issue should be reported if exceeded. See below for a full list.

Configuration can also be specified in a yaml format configuration file, provided by the `--config` option.
If no configuration file is provided and a `.bibl.yml` file is present in the current working directory, this file will
be used as a configuration file.
Command line option configuration will override configuration provided by a file.
See the default configuration [.bibl.yml](https://gitlab.com/arne.vandenkerchove/bibl/-/tree/master/bibl/.bibl.yml) for all values that can be overwritten in a configuration file.

Some rules, like the various `M01*`, `M02*` and `U01*` rules, are procedurally generated based on the `type_spec` setting.
This setting specifies which entry and field types should be present and can be modified to more easily ignore generated
rules for specific entry types or fields, or to add custom fields or entry types for which warnings should be given
while linting.

## CLI
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
  version       Show the package version.
```
```shell script
Usage: bibl lint [OPTIONS] [BIBLIOGRAPHY]...

  Lint a BibTeX bibliography file.

Options:
  --help  Show this message and exit.
```
```shell script
Usage: bibl list-all [OPTIONS]

  Show all available rules.

Options:
  -m      Format rules as markdown table.
  --help  Show this message and exit.
```
```shell script
Usage: bibl list-enabled [OPTIONS]

  Show all rules enabled by the configuration.

Options:
  -m      Format rules as markdown table.
  --help  Show this message and exit.
```

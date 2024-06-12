# bibla
https://github.com/MrClassicT/bibla/actions/runs/9430255754/artifacts/1581991547
![flake8](https://github.com/MrClassicT/bibla/actions/workflows/github-ci.yml/flake8-results/flake8.svg)
`bibla` is a minimalistic linter (style checker) for [biblatex](http://www.biblatex.org/) files with support for libraries
managed by [JabRef](https://www.jabref.org/).

`bibla` does not come with its own biblatex parser, but leverages the [pybtex](https://pybtex.org/) parser.

Bibla is an extension of bibl, which was made by Arne Van Den Kerckhove. The original Bibl can be found [here](https://gitlab.com/arnevdk/bibl). I do not claim any form of ownership over the original Bibl, I have only made some changes to it. Those changes I do claim ownership over. Just like the original Bibl, this will also be licensed under the MIT license.

## Installation

```shell script
pip install bibla
```
## Usage - This still needs to receive an update!

Run bibla on your biblatex files with the following command
```shell script
bibla lint bibliography1.bib
```
or
```shell script
bibla lint bibliography1.bib bibliography2.bib ... 
```
or as a python module with
```shell script
python -m bibla lint bibliography1.bib bibliography2.bib ... 
```

bibla will check these files for a variety of style issues and deviations from the biblatex spec (http://www.biblatex.org/Format/, https://en.wikipedia.org/wiki/biblatex).
Each possible type of issue is formulated as a rule. Each rule is identified by a unique code. Some examples of rules are 

Rule ID|Rule description
-|-
`U00`|Unrecognized entry type
`T01`|Non-standard whitespace at beginning of line (indents should be 2 spaces)
`T02`|Whitespace at end of line
`M01OnlineUrl`|Missing required field `url` for entry type `online`
`M02InbookPages`|Missing optional field `pages` for entry type `inbook`
`E08`|`pages` field formatting is incorrect. Please use the following format: 123--456. In ascending order seperated with two dashes.
`E09`|Entry should use correct date format: YYYY-MM-DD, YYYY-MM or YYYY!
`E10ArticleJournal`|Use `journaltitle` instead of `journal`!
...|...

This link provides a [list of all available rules](https://mrclassict.github.io/bibla/rules)
generated with the default configuration (see Configuration section below).


The first character of a rule id refers to a rules category, e.g. `E` for issues with entry values, `T` for textual
issues with the `.bib` file, etc.
**NOTE: The following does not work yet due to having a fixed set ignore in the general config, this will be fixed!** - May 18th, 2024
You can specify which rules to check by using `--select` or `--ignore`. Wildcards are allowed. `--select` will only
enable the specified rules, disabling all other rules, while `--ignore` will disable all rules except the ones specified.
`--select` and `--ignore` may not be specified simultaneously.
```shell script
bibla --select "D*,E06,T01" lint bibliography.bib
```
will only check all rules starting with D, rule E06 and rule T01
```
bibla --ignore "D*,E06,T01" lint bibliography.bib
```
will check all rules except all rules starting with D, rule E06 and rule T01

## Configuration

Aside from `--select` and `--ignore`, other configuration options can be provided via the cli, like `--max-line-length`
to specify the line length for which an issue should be reported if exceeded. See below for a full list.

Configuration can also be specified in a yaml format configuration file, provided by the `--config` option.
If no configuration file is provided and a `bibla.yml` or `.bibla.yml` file is present in the current working directory,
this file will be used as a configuration file.
Command line option configuration will override configuration provided by a file.
See the default configuration [bibla.yml](https://github.com/MrClassicT/bibla/blob/master/bibla/bibla.yml) for all values that can be overwritten in a configuration file.

Some rules, like the various `M01*`, `M02*` and `U01*` rules, are procedurally generated based on the `type_spec` setting.
This setting specifies which entry and field types should be present and can be modified to more easily ignore generated
rules for specific entry types or fields, or to add custom fields or entry types for which warnings should be given
while linting.

## CLI
```shell script
Usage: bibla [OPTIONS] COMMAND [ARGS]...

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
  lint          Lint a biblatex bibliography file.
  list-all      Show all available rules.
  list-enabled  Show all rules enabled by the configuration.
  version       Show the package version.
```
```shell script
Usage: bibla lint [OPTIONS] [BIBLIOGRAPHY]...

  Lint a biblatex bibliography file.

Options:
  --help  Show this message and exit.
```
```shell script
Usage: bibla list-all [OPTIONS]

  Show all available rules.

Options:
  -m      Format rules as markdown table.
  --help  Show this message and exit.
```
```shell script
Usage: bibla list-enabled [OPTIONS]

  Show all rules enabled by the configuration.

Options:
  -m      Format rules as markdown table.
  --help  Show this message and exit.
```

import unittest
import os
import tempfile

from bibla.lint import lint

UNKNOWN_ENTRY_TYPE_RULE_ID = 'U00'
UNRECOGNIZED_INPROCEEDINGS_FIELD_RULE_ID = 'U01Inproceedings'


class TestBase(unittest.TestCase):

    def lint_temporary_bibliography(self, content):
        bib_file = tempfile.NamedTemporaryFile('w', suffix='.bib', delete=False)
        bibliography = bib_file.name

        try:
            with bib_file:
                bib_file.write(content)
            return lint(bibliography, verbose=False)
        finally:
            os.unlink(bibliography)

    def test_run(self):
        lint("test_data/mit.bib", verbose=False)

    def test_incorrect_syntax(self):
        lint("test_data/syntax.bib", verbose=False)
        
    def test_correct_bibLaTex(self):
        lint("test_data/bibLaTeX.bib", verbose=False)

    def test_proceedings_entry_type_is_recognized(self):
        warnings = self.lint_temporary_bibliography("""@proceedings{proceedings-key,
  title = {Proceedings of the Test Conference},
  date = {2024},
}
""")

        self.assertNotIn(UNKNOWN_ENTRY_TYPE_RULE_ID, [warning.rule.rule_id for warning in warnings])

    def test_crossref_field_is_recognized(self):
        warnings = self.lint_temporary_bibliography("""@proceedings{proceedings-key,
  title = {Proceedings of the Test Conference},
  date = {2024},
}

@inproceedings{paper-key,
  title = {Paper Title},
  booktitle = {Proceedings of the Test Conference},
  date = {2024},
  crossref = {proceedings-key},
}
""")

        self.assertNotIn(UNRECOGNIZED_INPROCEEDINGS_FIELD_RULE_ID, [warning.rule.rule_id for warning in warnings])


if __name__ == '__main__':
    unittest.main()

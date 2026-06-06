import unittest
import os
import tempfile

from bibla.lint import lint


class TestBase(unittest.TestCase):

    def test_run(self):
        lint("test_data/mit.bib", verbose=False)

    def test_incorrect_syntax(self):
        lint("test_data/syntax.bib", verbose=False)
        
    def test_correct_bibLaTex(self):
        lint("test_data/bibLaTeX.bib", verbose=False)

    def test_proceedings_entry_type_is_recognized(self):
        with tempfile.NamedTemporaryFile('w', suffix='.bib', delete=False) as bib_file:
            bib_file.write("""@proceedings{proceedings-key,
  title = {Proceedings of the Test Conference},
  date = {2024},
}
""")
            bibliography = bib_file.name

        try:
            warnings = lint(bibliography, verbose=False)
        finally:
            os.unlink(bibliography)

        self.assertNotIn('U00', [warning.rule.rule_id for warning in warnings])

    def test_crossref_field_is_recognized(self):
        with tempfile.NamedTemporaryFile('w', suffix='.bib', delete=False) as bib_file:
            bib_file.write("""@proceedings{proceedings-key,
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
            bibliography = bib_file.name

        try:
            warnings = lint(bibliography, verbose=False)
        finally:
            os.unlink(bibliography)

        self.assertNotIn('U01Inproceedings', [warning.rule.rule_id for warning in warnings])


if __name__ == '__main__':
    unittest.main()

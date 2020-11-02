import unittest

from bibl.lint import bibl


class TestBase(unittest.TestCase):

    def test_run(self):
        bibl("resources/mit.bib", None)

    def test_jabref(self):
        bibl("resources/bci.bib", None)

    def test_incorrect_syntax(self):
        bibl("resources/syntax.bib", None)


if __name__ == '__main__':
    unittest.main()

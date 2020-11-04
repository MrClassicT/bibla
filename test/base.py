import unittest

from bibl.lint import lint


class TestBase(unittest.TestCase):

    def test_run(self):
        lint("resources/mit.bib")

    def test_jabref(self):
        lint("resources/bci.bib")

    def test_incorrect_syntax(self):
        lint("resources/syntax.bib")


if __name__ == '__main__':
    unittest.main()

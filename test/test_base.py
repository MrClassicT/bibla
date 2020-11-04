import unittest

from bibl.lint import lint


class TestBase(unittest.TestCase):

    def test_run(self):
        lint("test_data/mit.bib", output=False)

    def test_jabref(self):
        lint("test_data/bci.bib", output=False)

    def test_incorrect_syntax(self):
        lint("test_data/syntax.bib", output=False)


if __name__ == '__main__':
    unittest.main()

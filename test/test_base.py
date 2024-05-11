import unittest

from bibla.lint import lint


class TestBase(unittest.TestCase):

    def test_run(self):
        lint("test_data/mit.bib", verbose=False)

    def test_incorrect_syntax(self):
        lint("test_data/syntax.bib", verbose=False)
        
    def test_correct_bibLaTex(self):
        lint("test_data/bibLaTeX.bib", verbose=False)


if __name__ == '__main__':
    unittest.main()

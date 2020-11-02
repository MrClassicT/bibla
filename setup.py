from setuptools import setup

setup(
    name='bibl',
    version='0.1',
    description='A minimalistic bibtex linter',
    author='Arne Van Den Kerchove',
    author_email='arne@vandenkerchove.com',
    packages=['bibl'],
    install_requires=[
        'click',
        'pybtex',
        'pyyaml',
        'unidecode',
    ],
)

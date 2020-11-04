from setuptools import setup

setup(
    name='bibL',
    version='1.0',
    description='A minimalistic bibtex linter',
    url='https://gitlab.com/arne.vandenkerchove/biblint',
    author='Arne Van Den Kerchove',
    author_email='arne@vandenkerchove.com',
    packages=['bibl', 'bibl.rules'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'click',
        'fuzzywuzzy',
        'markdown-table',
        'pybtex',
        'pyyaml',
        'unidecode',
    ],
    entry_points={
        "console_scripts": ["bibl=bibl.__main__:cli"],
    },
)

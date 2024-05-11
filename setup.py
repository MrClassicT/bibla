"""`bibla` is a minimalistic linter (style checker) for BibLaTeX files. This is a fork of the original `bibla` by Arne Van Den Kerchove.

More information about bibla at https://gitlab.com/arne.vandenkerchove/bibla
"""

from setuptools import setup

with open("README.md", 'r') as readme:
    long_description = readme.read()

from bibla import __version__

setup(
    name='bibla',
    version=__version__,
    description='A minimalistic bibLaTeX linter based on bibla by Tristan Cuvelier.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MrClassicT/bibla',
    author='Tristan Cuvelier',
    author_email='tristan.cuvelier@student.hogent.be',
    packages=['bibla', 'bibla.rules'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'click>=7,<8',
        'fuzzywuzzy>=0.10,<1',
        'markdown-table',
        'pybtex==0.23.0',
        'pyyaml>=5,<6',
        'unidecode>=1,<2',
    ],
    extras_require={
        'dev': [
            'flake8',
            'pep8-naming',
            'flake8-docstrings',
            'anybadge',
            'markdown',
            'check-manifest',
            'twine',
        ]
    },
    entry_points={
        "console_scripts": ["bibla=bibla.__main__:cli"],
    },
    include_package_data=True,
    package_data={'': ['bibla.yml']}
)

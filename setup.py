from setuptools import setup

with open("README.md", 'r') as readme:
    long_description = readme.read()

from bibl import __version__

setup(
    name='bibL',
    version=__version__,
    description='A minimalistic bibtex linter',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/arne.vandenkerchove/biblint',
    author='Arne Van Den Kerchove',
    author_email='arne@vandenkerchove.com',
    packages=['bibl', 'bibl.rules'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
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
            'anybadge',
            'markdown',
            'check-manifest',
            'twine',
        ]
    },
    entry_points={
        "console_scripts": ["bibl=bibl.__main__:cli"],
    },
    include_package_data=True,
    package_data={'': ['.bibl.yml']}
)

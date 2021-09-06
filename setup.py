from setuptools import setup

setup(
        name='unfuck',
        version='1.0',
        description='A CLI tool to remove excess pages from PDFs',
        install_requires=['PyPDF2'],
        entry_points = {'console_scripts': ['unfuck=unfuck.cli:main']}
)

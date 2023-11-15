#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

requirements=[
    'pyModbusTCP==0.2.0',
    'typing_extensions==4.8.0',
]
test_requirements = [
    'pytest-cov',
    'pytest-mock',
    'pytest>=3',
]

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'etamodbus', '__version__.py')) as f:
    exec(f.read(), about)

with open('README.md', 'r') as fh:
    readme = fh.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    url=about['__url__'],
    packages=find_packages(),
    tests_require=test_requirements,
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
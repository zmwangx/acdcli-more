#!/usr/bin/env python3
"""Setup script for PyPI."""

import logging
import os
from setuptools import setup
import sys

PY_MAJOR_VERSION = sys.version_info[0]
if PY_MAJOR_VERSION < 3:
    logging.error("Incompatible with Python 2.x.")

here = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='acdcli-more',
    version='0.1-dev',
    description='More commands for acd_cli',
    long_description=long_description,
    url='https://github.com/zmwangx/acdcli-more',
    author='Zhiming Wang',
    author_email='zmwangx@gmail.com',
    license='GPLv2+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Archiving :: Backup',
    ],
    keywords=['amazon cloud drive'],
    packages=['acdcli_more'],
    install_requires=[
        'acdcli>=0.3.1',
        'appdirs',
        'zmwangx>=0.1.57+ge793724',
    ],
    entry_points={
        'console_scripts': [
            'acdcli-trees=acdcli_more.trees:main',
        ]
    },
    dependency_links = [
        'git+https://github.com/zmwangx/pyzmwangx.git@master#egg=zmwangx-0.1.57',
    ],
)

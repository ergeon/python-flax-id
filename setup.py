#!/usr/bin/env python

import codecs
import os
import re

from setuptools import setup


DIRNAME = os.path.dirname(__file__)


def rel(*parts):
    return os.path.abspath(os.path.join(DIRNAME, *parts))

with codecs.open(rel('README.md'), encoding='utf-8') as handler:
    DESCRIPTION = handler.read()

with open(rel('flax_id', '__init__.py')) as handler:
    INIT_PY = handler.read()

VERSION = re.findall("__version__ = '([^']+)'", INIT_PY)[0]


setup(
    name='python-flax-id',
    version=VERSION,
    description='Python implementation of Flax ID algorithm',
    long_description=DESCRIPTION,

    author='Ezhome Engineers',
    author_email='engineers@ezhome.com',
    url='https://github.com/ezhome/python-flax-id',

    include_package_data=True,
    install_requires=[],
    packages=[
        'flax_id',
        'flax_id/django'
    ],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords='ezhome flax flax-id',
    license='Other/Proprietary License',
    platforms='any',
)

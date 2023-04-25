import os
import re
import codecs
from setuptools import setup

NAME = 'ratr0_utils'
PACKAGES = ['ratr0.util']
DESCRIPTION = 'ratr0-utils is a collection of utilities for game development using the RATR0 engine'
LICENSE = 'GPL V3'
URI = 'https://github.com/weiju/ratr0-utils'
AUTHOR = 'Wei-ju Wu'
VERSION = '0.1.7'

KEYWORDS = ['ratr0', 'amiga', 'game', 'development', 'classic', 'ecs', 'aga']

# See trove classifiers
# https://testpypi.python.org/pypi?%3Aaction=list_classifiers

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Libraries :: Python Modules"
    ]
INSTALL_REQUIRES = ['pillow']

PACKAGE_DATA = {
    'ratr0.util': []
    }

if __name__ == '__main__':
    setup(name=NAME, description=DESCRIPTION,
          license=LICENSE,
          url=URI,
          version=VERSION,
          author=AUTHOR,
          author_email='weiju.wu@gmail.com',
          maintainer=AUTHOR,
          maintainer_email='weiju.wu@gmail.com',
          keywords=KEYWORDS,
          packages=PACKAGES,
          zip_safe=False,
          classifiers=CLASSIFIERS,
          install_requires=INSTALL_REQUIRES,
          include_package_data=True, package_data=PACKAGE_DATA,
          scripts=['bin/ratr0-maketiles',
                   'bin/ratr0-makesprites',
                   'bin/ratr0-makelevel',
                   'bin/ratr0-makeplanes',
                   'bin/ratr0-converttiled',
                   'bin/ratr0-file',
                   'bin/ratr0-wav2raw8'])

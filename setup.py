# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU Lesser General Public License as       |
# | published by the Free Software Foundation, either version 3 of the   |
# | License, or (at your option) any later version.                      |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU Lesser General Public License    |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
from os import path

here = path.abspath(path.dirname(__file__))

#### moved to markdown so we're not using the README as a long description
# it had too much info beyond the scope of the pure python package anyways
# Get the long description from the README.rst file
#with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#    long_description = f.read()
long_description = ""

if 'ROXCOMPOSER_VERSION' in os.environ:
    version = os.environ['ROXCOMPOSER_VERSION']
else:
    with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
        version = f.read()

version.strip()

setup(
    name='roxcomposer',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,

    description='droxIT microservice framework',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/droxit/roxcomposer',

    # Author details
    author='droxIT GmbH',
    author_email='info@droxit.de',

    # Choose your license
    license='LGPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Microservices',

        # Pick your license as you wish (should match "license" above)
        "License :: none - don't use it",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

    # What does your project relate to?
    keywords='microservice framework',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'protobuf>=3.3.*'
    ],

    python_requires='>=3.5',
    test_suite="roxcomposer.tests"
)

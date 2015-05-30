# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
from politicos import __version__


tests_require = [
    'mock',
    'nose',
    'coverage',
    'coveralls',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'sqltap',
    'factory_boy',
]

setup(
    name='politicos',
    version=__version__,
    description='Political data',
    long_description='''
Political data
''',
    keywords='political',
    author='Marcelo Jorge Vieira',
    author_email='metal@alucinados.com',
    url='https://github.com/olhoneles/politicos',
    license='AGPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'tornado>=4.1.0,<4.2.0',
        'cow-framework>=1.0.4,<1.1.0',
        'derpconf>=0.7.3,<0.8.0',
        'alembic>=0.7.6,<0.8.0',
        'mysql-python>=1.2.5,<1.3.0',
        'pycurl>=7.19.0,<7.20.0',
        'ujson>=1.33,<1.34.0',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            'politicos-api=politicos.server:main',
        ],
    },
)

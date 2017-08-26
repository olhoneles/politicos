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
        'Django>=1.10.7,<1.11.0',
        'django-localflavor>=1.2,<1.3.0',
        'django-bootstrap3>=6.2.2,<6.3.0',
        'django-tastypie>=0.13.3,<0.14.0',
        'django-tastypie-swagger==0.1.4-django1.10',
        'django-markup>=0.4,<0.5.0',
        'django-cors-headers>=1.1.0,<1.2.0',
        'django-cacheops>=3.2.1,<3.3.0',
        'django-extensions>=1.6.1,<1.7.0',
        'django-recaptcha>=1.0.5,<1.1.0',
        'derpconf>=0.8.0,<0.9.0',
        'Pygments>=2.0.2,<2.1.0',
        'psycopg2>=2.7.3,<2.8.0',
        'Markdown>=2.6.5,<2.7.0',
        'requests>=2.8.1,<2.9.0',
        'cssselect==0.9.1,<0.10.1',
        'lxml>=3.5.0,<3.6.0',
        'raven>=6.1.0,<6.2.0',
    ],
    dependency_links=[
        'https://github.com/olhoneles/django-tastypie-swagger/archive/fix-compatibility-django-1.10.zip#egg=django-tastypie-swagger-0.1.4-django1.10',
    ],
    extras_require={
        'tests': tests_require,
    },
)

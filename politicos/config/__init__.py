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


from derpconf.config import Config  # NOQA


Config.define(
    'SQLALCHEMY_CONNECTION_STRING',
    'mysql+mysqldb://root@localhost:3306/politicos',
    '',
    'DB'
)

Config.define(
    'SQLALCHEMY_POOL_SIZE',
    20,
    '',
    'DB'
)

Config.define(
    'SQLALCHEMY_POOL_MAX_OVERFLOW',
    10,
    '',
    'DB',
)

Config.define(
    'SQLALCHEMY_AUTO_FLUSH',
    True,
    'Defines whether auto-flush should be used in sqlalchemy',
    'DB'
)

Config.define(
    'COMMIT_ON_REQUEST_END',
    True,
    'Commit on request end',
    'DB'
)

Config.define(
    'ERROR_HANDLERS',
    [],
    'List of classes to handle errors',
    'General'
)

Config.define(
    'LOG_LEVEL',
    'ERROR',
    'Default log level',
    'Logging'
)
Config.define(
    'LOG_FORMAT',
    '%(asctime)s:%(levelname)s %(module)s - %(message)s',
    'Log Format to be used when writing log messages',
    'Logging'
)
Config.define(
    'LOG_DATE_FORMAT',
    '%Y-%m-%d %H:%M:%S',
    'Date Format to be used when writing log messages.',
    'Logging'
)

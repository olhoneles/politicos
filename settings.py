# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Affero General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
#  for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

from tornado.options import define, options

define('debug', default=True, help='debug mode')
define('port', default=8888, help='port to listen on', type=int)
define('redis_port', default=6379, help='redis port')
define('redis_host', default='localhost', help='redis hostname or IP')
define('es_hosts', default='localhost', help='elasticsearch hosts')
define('es_index', default='politicians', help='elasticsearch index')

options.parse_command_line()

define('per_page', default=10, help='items per page')
define('max_per_page', default=50, help='max items per page')

#!/usr/bin/env python3
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

import asyncio

from tornado.options import options
from tornado.log import enable_pretty_logging

import settings   # noqa: F401
from politicos_api.application import Application


def main():
    app = Application()
    app.listen(options.port)
    loop = asyncio.get_event_loop()
    app.init_with_loop(loop)

    enable_pretty_logging()

    if options.debug:
        env = 'development'
    else:
        env = 'production'

    print(f'Starting {env} server at http://localhost:{options.port}/')
    print('Quit the server with CONTROL-C.')

    loop.run_forever()


if __name__ == "__main__":
    main()

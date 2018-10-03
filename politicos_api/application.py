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

import aioredis
import tornado.web
from elasticsearch_async import AsyncElasticsearch
from tornado.options import options

from politicos_api.cache import RedisCacheBackend
from politicos_api.urls import handlers_api, handlers_website
from politicos_api.handlers.base import ErrorHandler


class Application(tornado.web.Application):

    def __init__(self):
        settings = dict(
            debug=options.debug,
            default_handler_class=ErrorHandler,
            default_handler_args=dict(status_code=404),
        )
        self.handlers_website = handlers_website
        self.handlers_api = handlers_api
        self.handlers = self.handlers_api + self.handlers_website
        tornado.web.Application.__init__(self, self.handlers, **settings)

    def init_with_loop(self, loop):
        self.redis = loop.run_until_complete(
            aioredis.create_redis(
                (options.redis_host, options.redis_port),
                loop=loop
            )
        )
        self.cache = RedisCacheBackend(self.redis)
        es_hosts = [x.strip() for x in options.es_hosts.split(',')]
        self.es = AsyncElasticsearch(hosts=es_hosts, loop=loop)

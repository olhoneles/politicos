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

from ujson import dumps
from urllib.parse import urlparse, urlencode, parse_qsl

from tornado.options import options
from tornado.template import Loader
from tornado.web import RequestHandler, ErrorHandler as BaseErrorHandler

from politicos_api.cache import CacheMixin


class BaseHandler(CacheMixin, RequestHandler):

    @property
    def es(self):
        return self.application.es

    async def prepare(self):
        self.page = int(self.get_argument('page', 1))

        # FIXME: lowercase
        self.per_page = int(self.get_argument('perPage', options.per_page))
        if self.per_page > options.max_per_page:
            self.per_page = options.per_page

        # FIXME: self.request.query_arguments
        # Validate fields in mapping?
        query_string = urlparse(self.request.query).path
        self.query_arguments = dict(parse_qsl(query_string))
        if 'page' in self.query_arguments:
            del self.query_arguments['page']
        if 'perPage' in self.query_arguments:
            del self.query_arguments['perPage']

        await super(BaseHandler, self).prepare()

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.set_header(
            'Access-Control-Allow-Headers',
            'access-control-allow-origin,authorization,content-type'
        )

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    async def json_response(self, data, status=200):
        self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.set_status(status)
        await self.write(dumps(data))

    def get_meta(self, result):
        # FIXME: is it for all items?
        try:
            total = result.get('hits', {}).get('total')
            url = self.reverse_url('main')
            _next = dict(page=self.page + 1, perPage=self.per_page)
            _next = {**_next, **self.query_arguments}
            next_url = f'{url}{urlencode(_next)}'
            if self.page > 1:
                previous = dict(page=self.page - 1, perPage=self.per_page)
                previous = {**previous, **self.query_arguments}
                previous_url = f'{url}{urlencode(previous)}'
            else:
                previous_url = None
        except AttributeError:
            total = len(result)
            previous_url = None
            next_url = None
            self.page = 1

        return {
            'next': None if total <= 0 else next_url,
            'page': self.page,
            'perPage': self.per_page,
            'previous': None if total <= 0 else previous_url,
            'total': total,
        }

    async def agg_query(self, fields):
        sources = []
        for x in fields:
            # FIXME: added way to integer fields
            sources.append(
                {x: {'terms': {'field': f'{x}.keyword', 'missing': True}}}
            )

        # FIXME: size (paginate)
        body = {
            'size': 0,
            'aggs': {
                'result': {
                    'composite': {
                        'size': 1000,
                        'sources': sources,
                    }
                }
            }
        }

        result = await self.es.search(
            index=options.es_index,
            body=body,
        )
        result = result \
            .get('aggregations', {}) \
            .get('result', {}) \
            .get('buckets', {})
        result = [x.get('key') for x in result]
        response = {
            'meta': self.get_meta(result),
            'objects': result,
        }
        return response


class ErrorHandler(BaseErrorHandler):
    def write_error(self, status_code, **kwargs):
        loader = Loader('politicos_api/templates')
        if status_code == 404:
            self.write(loader.load('404.html').generate())
        else:
            self.write(loader.load('error.html').generate())

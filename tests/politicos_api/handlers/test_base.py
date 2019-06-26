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
from unittest.mock import Mock, patch

from tornado.testing import gen_test

from politicos_api.handlers.base import BaseHandler
from tests.politicos_api.base import BaseTestCase


class BaseHandlerTestCase(BaseTestCase):
    def setUp(self):
        super(BaseHandlerTestCase, self).setUp()
        self.request = Mock()
        self.app = self.get_app()
        self.base_handler = BaseHandler(self.app, self.request)
        self.base_handler.page = 1
        self.base_handler.per_page = 10

    @patch("elasticsearch_async.AsyncElasticsearch.search")
    @gen_test
    async def test_agg_query(self, search_mock):
        f = asyncio.Future()
        es_response = {}
        f.set_result(es_response)
        search_mock.return_value = f

        response = await self.base_handler.agg_query([])
        self.assertEqual(
            response,
            {
                "meta": {
                    "next": None,
                    "page": 1,
                    "perPage": 10,
                    "previous": None,
                    "total": 0,
                },
                "objects": [],
            },
        )

    def test_get_meta(self):
        meta = self.base_handler.get_meta({})
        self.assertEqual(
            meta,
            {
                "next": None,
                "page": 1,
                "perPage": 10,
                "previous": None,
                "total": 0,
            },
        )

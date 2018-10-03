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
from ujson import loads
from unittest.mock import patch

from tests.politicos_api.base import BaseTestCase, get_json_mock


class MainHandlerTestCase(BaseTestCase):

    @patch('elasticsearch_async.AsyncElasticsearch.search')
    def test_main_handler(self, search_mock):
        f = asyncio.Future()
        es_main_response = get_json_mock('es_main_response.json')
        f.set_result(es_main_response)
        search_mock.return_value = f

        response = self.fetch('/api/v1/candidacies')

        self.assertEqual(response.code, 200)
        api_main_response = get_json_mock('api_main_response.json')
        self.assertEqual(loads(response.body), api_main_response)

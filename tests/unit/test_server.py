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

from cow.plugins.sqlalchemy_plugin import SQLAlchemyPlugin
from preggy import expect
from mock import patch

import politicos.server
from tests.unit.base import ApiTestCase


class ApiServerTestCase(ApiTestCase):
    def test_healthcheck(self):
        response = self.fetch('/healthcheck')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('WORKING')

    def test_server_handlers(self):
        srv = politicos.server.PoliticosApiServer()
        handlers = srv.get_handlers()

        expect(handlers).not_to_be_null()
        expect(handlers).to_length(13)

    def test_server_plugins(self):
        srv = politicos.server.PoliticosApiServer()
        plugins = srv.get_plugins()

        expect(plugins).to_length(1)
        expect(plugins[0]).to_equal(SQLAlchemyPlugin)

    @patch('politicos.server.PoliticosApiServer')
    def test_server_main_function(self, server_mock):
        politicos.server.main()
        expect(server_mock.run.called).to_be_true()

    def test_get_extra_server_parameters(self):
        srv = politicos.server.PoliticosApiServer()
        extra_server_parameters = srv.get_extra_server_parameters()

        expect(extra_server_parameters).to_length(1)
        expect(extra_server_parameters).to_be_like({'no_keep_alive': False})

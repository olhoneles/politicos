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

import os

from cow.testing import CowTestCase
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from politicos.config import Config
from politicos.server import PoliticosApiServer
from tests.fixtures import db


class ApiTestCase(CowTestCase):

    def drop_collection(self, document):
        document.objects.delete(callback=self.stop)
        self.wait()

    def tearDown(self):
        self.db.rollback()
        super(ApiTestCase, self).tearDown()

    def get_config(self):
        connection = "mysql+mysqldb://root@localhost:3306/test_politicos"
        return dict(
            SQLALCHEMY_CONNECTION_STRING=connection,
            SQLALCHEMY_POOL_SIZE=1,
            SQLALCHEMY_POOL_MAX_OVERFLOW=0,
            SQLALCHEMY_AUTO_FLUSH=True,
            COMMIT_ON_REQUEST_END=False,
        )

    def get_server(self):
        cfg = Config(**self.get_config())
        debug = os.environ.get('DEBUG_TESTS', 'False').lower() == 'true'
        self.server = PoliticosApiServer(config=cfg, debug=debug, db=db)
        return self.server

    def get_app(self):
        app = super(ApiTestCase, self).get_app()
        app.http_client = AsyncHTTPClient(self.io_loop)
        self.db = app.db
        return app

    @gen.coroutine
    def anonymous_fetch(self, url, *args, **kwargs):
        # ensure that the request has no cookies
        if 'headers' in kwargs and 'Cookie' in kwargs['headers']:
            del kwargs['headers']['Cookie']

        response = yield self.http_client.fetch(
            self.get_url(url), *args, **kwargs
        )
        raise gen.Return(response)

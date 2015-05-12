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

import logging

from ujson import dumps
from tornado.web import RequestHandler

from politicos import __version__


class BaseHandler(RequestHandler):

    @property
    def config(self):
        return self.application.config

    def initialize(self, *args, **kw):
        self.is_public = kw.pop('is_public', False)
        super(BaseHandler, self).initialize(*args, **kw)

    def log_exception(self, typ, value, tb):
        for handler in self.application.error_handlers:
            handler.handle_exception(
                typ, value, tb, extra={
                    'url': self.request.full_url(),
                    'ip': self.request.remote_ip,
                    'politicos-version': __version__
                }
            )

        super(BaseHandler, self).log_exception(typ, value, tb)

    def on_finish(self):
        if self.application.config.COMMIT_ON_REQUEST_END:
            if self.get_status() > 399:
                logging.debug('ROLLING BACK TRANSACTION')
                self.db.rollback()
            else:
                logging.debug('COMMITTING TRANSACTION')
                self.db.flush()
                self.db.commit()

    def options(self, *args):
        self.set_status(200)
        self.finish()

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS'
        )
        self.set_header('Access-Control-Allow-Headers', 'Accept, Content-Type')

    def write_json(self, obj):
        self.set_header("Content-Type", "application/json")
        self.write(dumps(obj))

    @property
    def db(self):
        return self.application.db

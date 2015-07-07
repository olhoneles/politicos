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

from ujson import loads
from tornado.gen import coroutine

from politicos.models.legislator import Legislator
from politicos.handlers import BaseHandler


class AllLegislatorsHandler(BaseHandler):

    @coroutine
    def get(self):
        query = self.db.query(Legislator)
        legislators = query.order_by(Legislator.name.asc()).all()

        if not legislators:
            self.write('{}')
            return

        result = [x.to_dict() for x in legislators]
        self.write_json(result)

    @coroutine
    def post(self):
        post_data = loads(self.request.body)

        name = post_data.get('name')

        if not name:
            self.set_status(400, 'Invalid legislator')
            return

        data = {
            'name': name,
            'picture': post_data.get('picture'),
            'website': post_data.get('website'),
            'email': post_data.get('email'),
            'gender': post_data.get('gender'),
            'date_of_birth': post_data.get('date_of_birth'),
            'about': post_data.get('about'),
        }

        legislator = Legislator.add_legislator(self.db, data)
        self.write_json(legislator.to_dict())

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

from tornado.gen import coroutine

from ujson import loads

from politicos.models.legislature import Legislature
from politicos.handlers import BaseHandler


class AllLegislaturesHandler(BaseHandler):

    @coroutine
    def get(self):
        query = self.db.query(Legislature)
        legislatures = query.order_by(Legislature.date_start.asc()).all()

        if not legislatures:
            self.write('{}')
            return

        result = [x.to_dict() for x in legislatures]
        self.write_json(result)

    @coroutine
    def post(self):
        post_data = loads(self.request.body)

        date_start = post_data.get('date_start')
        date_end = post_data.get('date_end')
        institution_id = post_data.get('institution_id')

        if not date_start or not date_end or not institution_id:
            self.set_status(400, 'Invalid Legislature')
            return

        data = {
            'date_start': date_start,
            'date_end': date_end,
            'institution_id': institution_id,
        }

        legislature = Legislature.add_legislature(self.db, data)
        self.write_json(legislature.to_dict())

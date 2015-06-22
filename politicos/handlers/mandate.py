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

from politicos.models.mandate import Mandate
from politicos.handlers import BaseHandler


class AllMandatesHandler(BaseHandler):

    @coroutine
    def get(self):
        query = self.db.query(Mandate)
        mandates = query.order_by(Mandate.date_start.asc()).all()

        if not mandates:
            self.write('{}')
            return

        result = [x.to_dict() for x in mandates]
        self.write_json(result)

    @coroutine
    def post(self):
        post_data = loads(self.request.body)

        date_start = post_data.get('date_start')
        date_end = post_data.get('date_end')
        political_office_id = post_data.get('political_office_id')
        legislator_id = post_data.get('legislator_id')

        if (not date_start or not date_end or not political_office_id or not
                legislator_id):
            self.set_status(400, 'Invalid Mandate')
            return

        data = {
            'date_start': date_start,
            'date_end': date_end,
            'political_office_id': political_office_id,
            'legislator_id': legislator_id,
        }

        mandate = Mandate.add_mandate(self.db, data)
        self.write_json(mandate.to_dict())

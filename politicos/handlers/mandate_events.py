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

from politicos.models.mandate_events import MandateEvents
from politicos.handlers import BaseHandler


class AllMandateEventsHandler(BaseHandler):

    @coroutine
    def get(self):
        query = self.db.query(MandateEvents)
        mandate_events = query \
            .order_by(MandateEvents.date.asc()) \
            .all()

        if not mandate_events:
            self.write('{}')
            return

        result = [x.to_dict() for x in mandate_events]
        self.write_json(result)

    @coroutine
    def post(self):
        post_data = loads(self.request.body)

        date = post_data.get('date')
        mandate_id = post_data.get('mandate_id')
        mandate_events_type_id = post_data.get('mandate_events_type_id')

        if not date or not mandate_events_type_id or not mandate_id:
            self.set_status(400, 'Invalid Mandate Events')
            return

        data = {
            'date': date,
            'mandate_id': mandate_id,
            'mandate_events_type_id': mandate_events_type_id
        }

        mandate_events = MandateEvents.add_mandate_events(self.db, data)
        self.write_json(mandate_events.to_dict())
